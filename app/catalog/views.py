# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils import simplejson
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_protect

from settings import *
from tools.zoook import siteConfiguration, checkPartnerID, checkFullName, connOOOP
from tools.paginator import *

from catalog.models import *

CATALOG_ORDERS = {
        'position':_('Position'),
        'price': _('Price'),
        'name': _('Name'),
    }

@login_required
def updateprice(request):
    """
    B2B features
    Update Price catalog/product if partner are price rules different price rule sale shop.
    http://domain.com/catalog/updateprice/
    Return dicc elements ID product-price
    """

    data = ''
    if 'ides' in request.GET:
        product_ids = request.GET.get('ides').split(',') # get values ids
        if len(product_ids):
            data = ProductProduct.update_prices(request, product_ids)

    return HttpResponse(data, mimetype='application/javascript')

def index(request):
    """
    Catalog Index
    All Categories list
    """

    values = ProductCategory.get_categories_list()

    site_configuration = siteConfiguration(SITE_ID)

    title = _('Categories')
    metadescription = _('List all categories of %s') % site_configuration.site_title
    return render_to_response("catalog/index.html", {
                    'title': title,
                    'metadescription': metadescription, 
                    'values': values,
                }, context_instance=RequestContext(request))

@csrf_protect
def category(request, category):
    """All Products filtered by category"""

    values = []

    if not category:
        raise Http404(_('This category is not available because you navigate with bookmarks or search engine. Use navigation menu'))

    kwargs = {
        'slug_'+get_language(): category, #slug is unique
        'status': True,
    }
    category = get_object_or_404(ProductCategory, **kwargs)
    categories_path = category.get_path() #pathway

    default = category.default_sort_by and category.default_sort_by or 'position'
    set_paginator_options(request, default)

    qtmpl, qprod = ProductTemplate.get_qattributes(request)

    products_tmpl = ProductTemplate.objects.filter(
            Q(**qtmpl),
            Q(**qprod),
            Q(product_product_set__active=True),
            Q(categ=category),
            Q(visibility='all') | 
            Q(visibility='catalog')
        )
    total = products_tmpl.count()

    # get price and base_image product
    for tplproduct in products_tmpl:
        product_products = tplproduct.product_product_set.order_by('price')
        if not product_products.count():
            continue
        base_image = product_products[0].get_base_image()
        values.append({
                'product': tplproduct,
                'name': tplproduct.name.lower(), 
                'product_variant': product_products.count(),
                'price': product_products[0].get_price(),
                'price_normal': product_products[0].price,
                'price_special': product_products[0].price_special,
                'position': tplproduct.position,
                'base_image': base_image
            })

    # == order by position, name or price ==
    try:
        values.sort(key=lambda x: x[request.session['order']], reverse = request.session['order_by'] == 'desc')
    except:
        pass

    # == template values ==
    num_pages = get_num_pages(products_tmpl, request.session['paginator'])
    title = _('%(category)s - Page %(page)s of %(total)s') % {
                'category': category.name,
                'page': int(request.GET.get('page', '1')),
                'total': num_pages
            }
    metadescription = _('%(category)s. Page %(page)s of %(total)s') % {
                'category': category.description and category.description or category.name,
                'page': int(request.GET.get('page', '1')),
                'total': num_pages
            }
    category_values = {
        'title': title,
        'category': category,
        'metadescription': metadescription,
        'values': values,
        'paginator_option': request.session['paginator'],
        'mode_option': request.session['mode'],
        'order_option': request.session['order'],
        'order_by_option': request.session['order_by'],
        'paginator_items': PAGINATOR_ITEMS,
        'catalog_orders': CATALOG_ORDERS,
        'total': total,
        'categories_path': categories_path,
        'currency': DEFAULT_CURRENCY,
    }
    return render_to_response("catalog/category.html", category_values, context_instance=RequestContext(request))

@csrf_protect
def product(request, product):
    """Product View"""

    kwargs = {
        'slug_'+get_language(): product, #slug is unique
    }

    tplproduct = get_object_or_404(ProductTemplate, **kwargs) #ProductTemplate

    # get products ordered by price, the first is the cheapest
    prods = tplproduct.product_product_set.order_by('price')

    base_image, thumb_images = prods[0].get_all_images()

    title = _('%(product)s') % {'product': tplproduct.name}
    if PRODUCT_METADESCRIPTION:
        metadescription = _('Buy %(name)s for %(price)s %(currency)s.') % {
                                'name': tplproduct.name,
                                'price': prods[0].price,
                                'currency': DEFAULT_CURRENCY.decode("utf-8"),
                        }
        if tplproduct.metadescription:
            metadescription = metadescription+' '+tplproduct.metadescription
    else:
        metadescription = '%(metadescription)s' % {'metadescription': tplproduct.metadescription}
    metakeywords = tplproduct.metakeyword and tplproduct.metakeyword or ''

    related_products = tplproduct.get_related_products()
    upsells_products = tplproduct.get_upsells_produts()

    #add session last visited
    tplproduct.set_last_visited(request, tplproduct)

    values = {
        'title': title,
        'metadescription': metadescription,
        'metakeywords': metakeywords,
        'product': tplproduct,
        'products': prods,
        'related_products': related_products,
        'upsells_products': upsells_products,
        'price': prods[0].get_price(),
        'price_normal': prods[0].price,
        'price_special': prods[0].price_special,
        'base_image': base_image,
        'thumb_images': thumb_images,
        'url': LIVE_URL,
        'currency': DEFAULT_CURRENCY,
        'twitter_user':TWITTER_USER,
    }
    return render_to_response("catalog/product.html", values, context_instance=RequestContext(request))

@login_required
def whistlist(request):
    """
    Whistlist
    Favourites products customer
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or contact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    prod_whistlist = False
    partner = conn.ResPartner.get(partner_id)
    product_obj = partner.product_whistlist_ids

    path = request.path_info.split('/')
    if 'remove' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if tplproduct.count() > 0:
            try:
                for prod in product_obj:
                    if prod.id == tplproduct[0].id: #exist this product whistlist
                        prod_whistlist = conn_webservice('res.partner','write', [[partner_id], {'product_whistlist_ids':[(3, tplproduct[0].id)]}])
            except:
                prod_whistlist = True
                
    if 'add' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if tplproduct.count() > 0:
            check_add = False
            if product_obj:
                for prod in product_obj:
                    if prod.id == tplproduct[0].id: #exist this product whistlist
                        check_add = True
            if not check_add:
                prod_whistlist = conn_webservice('res.partner','write', [[partner_id], {'product_whistlist_ids':[(4, tplproduct[0].id)]}])

    title = _('Whislist')
    metadescription = _('Whislist of %s') % full_name
    
    if prod_whistlist:
        partner = conn.ResPartner.get(partner_id) #refresh product_whistlist_ids if add or remove
        product_obj = partner.product_whistlist_ids
    
    products = []
    if product_obj:
        for prod in product_obj:
            prods = ProductProduct.objects.filter(product_tmpl=prod.id).order_by('price')
            tplproduct = ProductTemplate.objects.get(id=prod.id)
            prod_images = ProductImages.objects.filter(product=prod.id,exclude=False)
            base_image = False
            if prod_images.count() > 0:
                base_image = prod_images[0]

            products.append({'product': tplproduct, 'name': tplproduct.name, 'price': prods[0].price, 'base_image': base_image})

    return render_to_response("catalog/whistlist.html", {
                    'title': title, 'metadescription': metadescription, 
                    'products': products,
                    'currency': DEFAULT_CURRENCY,
                }, context_instance=RequestContext(request))

def compare(request):
    """
    Compare products
    """

    site_configuration = siteConfiguration(SITE_ID)

    values = []
    products = []

    if 'compare' in request.session:
        products = request.session['compare']

    path = request.path_info.split('/')
    if 'remove' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if tplproduct.count() > 0:
            try:
                products.remove(tplproduct[0].id)
            except:
                pass

    if 'add' in path:
        kwargs = {
            'slug_'+get_language(): path[-1], #slug is unique
        }
        tplproduct = ProductTemplate.objects.filter(**kwargs)
        if tplproduct.count() > 0:
            products.append(tplproduct[0].id)

    products = [x for x in set(products)]
    products = request.session['compare'] = products

    products_tmpl = ProductTemplate.objects.filter(id__in=products)

    # get price and base_image product
    for tplproduct in products_tmpl:
        product_products = tplproduct.product_product_set.order_by('price')
        if not product_products.count():
            continue
        base_image = product_products[0].get_base_image()
        values.append({
                'product': tplproduct,
                'name': tplproduct.name.lower(), 
                'product_variant': product_products.count(),
                'price': product_products[0].price,
                'price_normal': product_products[0].price,
                'price_special': product_products[0].price_special,
                'position': tplproduct.position,
                'base_image': base_image,
            })

    title = _('Compare Products')
    metadescription = _('Compare products of %s') % site_configuration.site_title

    return render_to_response("catalog/compare.html", {
                    'title': title,
                    'metadescription': metadescription,
                    'products': values,
                    'currency': DEFAULT_CURRENCY,
                }, context_instance=RequestContext(request))

def manufacturers(request, key=False):
    """All Manufacturers
    List all manufacturers. Available with Pagination
    :param request
    :return render_to_response
    """

    site_configuration = siteConfiguration(SITE_ID)

    manufacturers = ResManufacturer.objects.all()
    manufacturers = ResManufacturer.objects.filter(active=True).order_by('name')

    num_pages = get_num_pages(manufacturers, PAGINATOR_MANUFACTURER_TOTAL)
    title = _('Manufacturers on %(site)s - Page %(page)s of %(total)s') % {
                            'site': site_configuration.site_title,
                            'page': int(request.GET.get('page', '1')),
                            'total': num_pages
                        }
    metadescription = _('Manufacturers of %(site)s - Page %(page)s of %(total)s') % {
                            'site': site_configuration.site_title,
                            'page': int(request.GET.get('page', '1')),
                            'total': num_pages
                        }
    return render_to_response("catalog/manufacturers.html", {
                            'title':title, 
                            'metadescription': metadescription,
                            'site': site_configuration.site_title,
                            'manufacturers': manufacturers,
                        },
                        context_instance=RequestContext(request))

def manufacturer(request, manufacturer):
    """Manufacturer Detail and Products
    :param request
    :param manufacturer
    :return render_to_response
    """

    values = []

    site_configuration = siteConfiguration(SITE_ID)

    kwargs = {
        'slug': manufacturer, #slug is unique
    }
    if not request.user.is_staff:
        kwargs['active'] = True
    manufacturer = get_object_or_404(ResManufacturer, **kwargs)

    default = 'position'
    set_paginator_options(request, default)

    #top category manufacturer
    categories_manufacturer = []
    top = ProductCategory.objects.filter(parent=None)
    categories = ProductCategory.objects.filter(parent=top[0],status=True).order_by('position')
    for category in categories:
        products_tmpl = ProductTemplate.objects.filter(
            Q(manufacturer=manufacturer),
            Q(product_product_set__active=True),
            Q(categ=category),
            Q(visibility='all') | 
            Q(visibility='catalog')
        )
        total = products_tmpl.count()
        categories_manufacturer.append([category,total])

    qtmpl, qprod = ProductTemplate.get_qattributes(request)

    products_tmpl = ProductTemplate.objects.filter(
        Q(**qtmpl),
        Q(**qprod),
        Q(manufacturer=manufacturer),
        Q(product_product_set__active=True),
        Q(visibility='all') | 
        Q(visibility='catalog')
    )
    total = products_tmpl.count()

    # get price and base_image product
    for tplproduct in products_tmpl:
        product_products = tplproduct.product_product_set.order_by('price')
        if not product_products.count():
            continue
        base_image = product_products[0].get_base_image()
        values.append({
                'product': tplproduct,
                'name': tplproduct.name.lower(), 
                'product_variant': product_products.count(),
                'price': product_products[0].get_price(),
                'price_normal': product_products[0].price,
                'price_special': product_products[0].price_special,
                'position': tplproduct.position,
                'base_image': base_image
            })

    # == order by position, name or price ==
    values.sort(key=lambda x: x[request.session['order']], reverse = request.session['order_by'] == 'desc')

    num_pages = get_num_pages(products_tmpl, request.session['paginator'])

    title = _("%(manufacturer)s - %(site)s - Page %(page)s of %(total)s") % {
        'manufacturer': manufacturer.name,
        'site': site_configuration.site_title,
        'page': int(request.GET.get('page', '1')),
        'total': num_pages,
    }
    metadescription = _('Buy %(name)s on %(site)s. Page %(page)s of %(total)s') % {
            'name': manufacturer.name,
            'site': site_configuration.site_title,
            'page': int(request.GET.get('page', '1')),
            'total': num_pages,
    }
    metakeywords = manufacturer.name
    
    change_manufacturer = request.user.has_perm('catalog.change_resmanufacturer')

    values = {
        'title':title,
        'metakeywords':metakeywords,
        'metadescription':metadescription,
        'manufacturer':manufacturer,
        'categories': categories_manufacturer,
        'values': values,
        'total': total,
        'order_option': request.session['order'],
        'order_by_option': request.session['order_by'],
        'paginator_option': request.session['paginator'],
        'paginator_items': PAGINATOR_ITEMS,
        'currency': DEFAULT_CURRENCY,
        'catalog_orders': CATALOG_ORDERS,
        'change_manufacturer': change_manufacturer,
    }

    return render_to_response("catalog/manufacturer.html", values, context_instance=RequestContext(request))

# =====================================
# Catalog Management Views
# =====================================
"""
Products Home Form. Add/Edit
"""

class ProductHomeForm(ModelForm):
    class Meta:
        model = ProductHome
    
@login_required
def product_home(request, home_id=False):
    """
    Product Home
    """
    values = ProductHome.objects.all().order_by('-order')

    return render_to_response("catalog/form_list.html", {
                            'title':_('Product Home'),
                            'app': 'producthome',
                            'values': values,
                        },
                        context_instance=RequestContext(request))

def product_home_form(request, home_id):
    """
    Product Home Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if home_id:
            home = ProductHome.objects.get(id=home_id)
            form = ProductHomeForm(request.POST, instance=home)
        else:
            form = ProductHomeForm(request.POST, request.FILES)

        if form.is_valid():
            home = form.save()

            if LOCALE_URI:
                redirect = "%s/catalogmanage/producthome/" % (context_instance['LOCALE_URI'])
            else:
                redirect = "catalogmanage/producthome/"
    else:
        if home_id:
            home = get_object_or_404(ProductHome,id=home_id)
            form = ProductHomeForm(instance=home)
        else:
            form = ProductHomeForm()
    return form, redirect

@login_required
def product_home_add(request):
    """
    Product Home Add
    """
    home = False
    context_instance=RequestContext(request)
    
    if not request.user.has_perm('catalog.add_producthome'):
        raise Http404
    form, redirect = product_home_form(request, home)
    if redirect:
        return HttpResponseRedirect(redirect)
        
    if LOCALE_URI:
        url_form = '%s/catalogmanage/producthome/add/' % (context_instance['LOCALE_URI'])
    else:
        url_form = 'catalogmanage/producthome/add/'

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Add Product Home'),
                            }, context_instance=RequestContext(request))

@login_required
def product_home_edit(request, home_id):
    """
    Product Home Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('catalog.change_producthome'):
        raise Http404

    try:
        home_id = int(home_id)
    except ValueError:
        raise Http404

    form, redirect = product_home_form(request, home_id)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/catalogmanage/producthome/edit/%s' % (context_instance['LOCALE_URI'], home_id)
    else:
        url_form = 'catalogmanage/producthome/edit/%s' % (home_id)

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Edit Product Home'),
                            }, context_instance=RequestContext(request))

"""
Product Recommended Form. Add/Edit
"""

class ProductRecommendedForm(ModelForm):
    class Meta:
        model = ProductRecommended
    
@login_required
def product_recommended(request, recommended_id=False):
    """
    Product Recommended
    """
    values = ProductRecommended.objects.all().order_by('-order')

    return render_to_response("catalog/form_list.html", {
                            'title':_('Product Recommended'),
                            'app': 'productrecommended',
                            'values': values,
                        },
                        context_instance=RequestContext(request))

def product_recommended_form(request, recommended_id):
    """
    Recommended Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if recommended_id:
            recommended = ProductRecommended.objects.get(id=recommended_id)
            form = ProductRecommendedForm(request.POST, instance=recommended)
        else:
            form = ProductRecommendedForm(request.POST, request.FILES)

        if form.is_valid():
            recommended = form.save()

            if LOCALE_URI:
                redirect = "%s/catalogmanage/productrecommended/" % (context_instance['LOCALE_URI'])
            else:
                redirect = "catalogmanage/productrecommended/"
    else:
        if recommended_id:
            recommended = get_object_or_404(ProductRecommended,id=recommended_id)
            form = ProductRecommendedForm(instance=recommended)
        else:
            form = ProductRecommendedForm()
    return form, redirect

@login_required
def product_recommended_add(request):
    """
    Product Recommended Add
    """
    recommended = False
    context_instance=RequestContext(request)
    
    if not request.user.has_perm('catalog.add_productrecommended'):
        raise Http404
    form, redirect = product_recommended_form(request, recommended)
    if redirect:
        return HttpResponseRedirect(redirect)
        
    if LOCALE_URI:
        url_form = '%s/catalogmanage/productrecommended/add/' % (context_instance['LOCALE_URI'])
    else:
        url_form = 'catalogmanage/productrecommended/add/'

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Add Product Recommended'),
                            }, context_instance=RequestContext(request))

@login_required
def product_recommended_edit(request, recommended_id):
    """
    Product Recommended Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('catalog.change_productrecommended'):
        raise Http404

    try:
        recommended_id = int(recommended_id)
    except ValueError:
        raise Http404

    form, redirect = product_recommended_form(request, recommended_id)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/catalogmanage/productrecommended/edit/%s' % (context_instance['LOCALE_URI'], recommended_id)
    else:
        url_form = 'catalogmanage/productrecommended/edit/%s' % (recommended_id)

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Edit Product Recommended'),
                            }, context_instance=RequestContext(request))

"""
Product Offer Form. Add/Edit
"""

class ProductOfferForm(ModelForm):
    class Meta:
        model = ProductOffer
    
@login_required
def product_offer(request, offer_id=False):
    """
    Product Offer
    """
    values = ProductOffer.objects.all().order_by('-order')

    return render_to_response("catalog/form_list.html", {
                            'title':_('Product Offer'),
                            'app': 'productoffer',
                            'values': values,
                        },
                        context_instance=RequestContext(request))

def product_offer_form(request, offer_id):
    """
    Product Offer Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if offer_id:
            offer = ProductOffer.objects.get(id=offer_id)
            form = ProductOfferForm(request.POST, instance=offer)
        else:
            form = ProductOfferForm(request.POST, request.FILES)

        if form.is_valid():
            offer = form.save()

            if LOCALE_URI:
                redirect = "%s/catalogmanage/productoffer/" % (context_instance['LOCALE_URI'])
            else:
                redirect = "catalogmanage/productoffer/"
    else:
        if offer_id:
            offer = get_object_or_404(ProductOffer,id=offer_id)
            form = ProductOfferForm(instance=offer)
        else:
            form = ProductOfferForm()
    return form, redirect

@login_required
def product_offer_add(request):
    """
    Offer Add
    """
    offer = False
    context_instance=RequestContext(request)
    
    if not request.user.has_perm('catalog.add_productoffer'):
        raise Http404
    form, redirect = product_offer_form(request, offer)
    if redirect:
        return HttpResponseRedirect(redirect)
        
    if LOCALE_URI:
        url_form = '%s/catalogmanage/productoffer/add/' % (context_instance['LOCALE_URI'])
    else:
        url_form = 'catalogmanage/productoffer/add/'

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Add Product Offer'),
                            }, context_instance=RequestContext(request))

@login_required
def product_offer_edit(request, offer_id):
    """
    Product Offer Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('catalog.change_productoffer'):
        raise Http404

    try:
        offer_id = int(offer_id)
    except ValueError:
        raise Http404

    form, redirect = product_offer_form(request, offer_id)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/catalogmanage/productoffer/edit/%s' % (context_instance['LOCALE_URI'], offer_id)
    else:
        url_form = 'catalogmanage/productoffer/edit/%s' % (offer_id)

    return render_to_response('catalog/form.html', {
                                'form':form,
                                'url_form':url_form,
                                'title':_('Edit Product Offer'),
                            }, context_instance=RequestContext(request))
