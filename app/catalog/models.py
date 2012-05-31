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

from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from django.utils.translation import get_language, ugettext_lazy as _

from tools.conn import conn_webservice
from transmeta import TransMeta
from transurl import catalog_url, product_url, manufacturer_url

from settings import LIVE_URL, LOCALE_URI, OERP_SALE

from datetime import datetime

import tools.cms.enums as enums
import simplejson as json

'''OpenERP Models'''
class ProductCategory(models.Model):
    """ProductCategory OpenERP"""
    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=128, help_text=_("This is a unique identifier that allows your contents to display its detail view, ex 'how-can-i-contribute'"), unique=True)
    fslug = models.CharField(_('Full Slug'), max_length=256, null=True, blank=True)
    metatitle = models.CharField(_('Title'), max_length=128, null=True, blank=True)
    metakeyword = models.TextField(_('Keyword'), null=True, blank=True)
    metadescription = models.TextField(_('Description'), null=True, blank=True)
    DEFAULT_SORT_BY_CHOICES = (
        ('default', 'Use Config Settings'),
        ('position', 'Position'),
        ('name', 'Name'),
        ('price', 'Price')
    )
    default_sort_by = models.CharField(_('Default Product Listing Sort (Sort By)'), choices=DEFAULT_SORT_BY_CHOICES,  default='default', max_length=40)
    status = models.BooleanField(_('Status'), default=False)
    parent = models.ForeignKey('ProductCategory', null=True, blank=True)
    position = models.IntegerField(_('Sequence'), null=True, blank=True)
    
    """ Custom fields model """

    class Meta:
        db_table = 'product_category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        translate = (
            'name',
            'description',
            'slug',
            'fslug',
            'metatitle',
            'metakeyword',
            'metadescription',
            )
        ordering = ['-position']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if LOCALE_URI:
            url = '/%s/%s/%s' % (get_language(), catalog_url[get_language()], self.fslug)
        else:
            url = '/%s/%s' % (catalog_url[get_language()], self.fslug)
        return url

    def collect_children(self, level = 0, children = []):
        """Category Children.
        Inv: Children nodes are stored in the list children"""

        values = ProductCategory.objects.filter(parent=self,status=True).order_by('position')
        for child in values:
            children.append((child.id, level))
            child.collect_children(level + 1, children)
        return children # Not necessary, but clearer width return

    @staticmethod
    def get_categories_list():
        values = []
        try:
            root_category = ProductCategory.objects.get(parent = None)
            categories = root_category.collect_children(level=1, children = [])
            oldlevel = 0
            for (category, level) in categories:
                values.append((ProductCategory.objects.get(id=category), level, oldlevel))
                oldlevel = level
        except ObjectDoesNotExist:
            pass
        return values

    def get_path(self):
        """Category Path
        When return, parent category omited by slice
        path from parent -> children
        :return [{'name','fslug'}]
        """

        categories = ProductCategory.objects.filter(id = self.id)
        path = []
        path.append({'name':categories[0].name,'fslug':categories[0].fslug})

        while categories[0].parent:
            categories = ProductCategory.objects.filter(id = categories[0].parent.id)
            path.insert(0, {'name':categories[0].name,'fslug':categories[0].fslug})
        return path[1:]

class ProductTemplate(models.Model):
    """ProductTemplate OpenERP"""
    __metaclass__ = TransMeta

    created_on = models.DateTimeField(_('created on'), default=datetime.now, editable=False)
    name = models.CharField(_('Name'), max_length=128)
    codes = models.TextField(_('Codes'), null=True, blank=True, help_text=_("Separated by comma"))
    categ = models.ManyToManyField('ProductCategory', null=True, blank=True, related_name='product_template_set')
    shortdescription = models.TextField(_('Short Description'), null=True, blank=True)
    description = models.TextField(_('Sale Description'), null=True, blank=True)
    slug = models.CharField(_('Slug'), max_length=128, null=True, blank=True)
    VISIBILITY_CHOICES = (
        ('all', 'All'),
        ('search', 'Search'),
        ('catalog', 'Catalog'),
        ('none', 'None'),
    )
    visibility = models.CharField(_('Visibility'), choices=VISIBILITY_CHOICES, default='', max_length=40)
    metatitle = models.CharField(_('Meta Title'), max_length=128, null=True, blank=True)
    metadescription = models.TextField(_('Meta Description'), null=True, blank=True)
    metakeyword = models.TextField(_('Meta Keyword'), null=True, blank=True)
    crosssells = models.ManyToManyField('ProductTemplate', blank=True, related_name='crosssells_set')
    related = models.ManyToManyField('ProductTemplate', blank=True, related_name='related_set')
    upsells = models.ManyToManyField('ProductTemplate', blank=True, related_name='upsells_set')
    uom = models.CharField(_('Unit Of Measure'), max_length=128)
    uos = models.CharField(_('Unit of Sale'), max_length=128)
    volume = models.FloatField(_('Volume'), null=True, blank=True)
    warranty = models.FloatField(_('Warranty (months)'),null=True, blank=True)
    weight = models.FloatField(_('Gross weight'),null=True, blank=True)
    weight_net = models.FloatField(_('Net weight'), null=True, blank=True)
    status = models.BooleanField(_('Status'), default=False)
    position = models.SmallIntegerField(_('Position'), default=100)
    newproduct = models.BooleanField(_('New'), default=False)
    manufacturer = models.ForeignKey('ResManufacturer', null=True, blank=True, related_name='res_manufacturer_set')

    """ Custom fields model """

    class Meta:
        db_table = 'product_template'
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        translate = (
            'name',
            'slug',
            'shortdescription',
            'description',
            'metadescription',
            'metakeyword',
            'metatitle',
        )
        ordering = ['-created_on']

    def __unicode__(self):
        return self.name

    def save(self):
        self.created_on = datetime.now()
        super(ProductTemplate, self).save()

    def get_absolute_url(self):
        if LOCALE_URI:
            url = '/%s/%s/%s' % (get_language(), product_url[get_language()], self.slug)
        else:
            url = '/%s/%s' % (product_url[get_language()], self.slug)
        return url

    def get_related_products(self):
        related_products = []
        for prod_template_related in self.related.all():
            products = prod_template_related.product_product_set.order_by('price')
            related_products.append({'product':prod_template_related, 'products':products})
        return related_products

    def get_upsells_produts(self):
        upsells_products = []
        for prod_template_upsell in self.upsells.all():
            products = prod_template_upsell.product_product_set.order_by('price')
            upsells_products.append({'product':prod_template_upsell, 'products':products})
        return upsells_products

    def set_last_visited(self, request, tplproduct):
        """Set last visited products template
        :param request
        :param tplproduct
        return list of IDs last 25 products visited
        """
        last_visited = request.session.get('last_visited', [])
        if tplproduct.id not in last_visited:
            last_visited.append(tplproduct.id)
            last_visited = last_visited[-25:]

        request.session['last_visited'] = last_visited
        return last_visited

    @staticmethod
    def get_qattributes(request):

        prod_template_fields = ProductTemplate._meta.get_all_field_names()
        prod_fields = ProductProduct._meta.get_all_field_names()
        #search products by attributes
        qtmpl = {}
        qprod = {}

        field_int = [
            'ForeignKey',
            'ManyToManyField',
        ]
        parameters = request.GET
        if len(parameters.keys()) > 0:
            for key, value in parameters.iteritems():
                if key[:2] == 'x_': #product product. Only fields start by x_ (product attribute)
                    if key in prod_fields:
                        if ProductProduct._meta.get_field(key).get_internal_type() in field_int:
                            try:
                                value = int(value)
                            except ValueError:
                                value = False
                        if value:
                            qprod['product_product_set__'+key] = value
                else: #product template
                    if key in prod_template_fields:
                        if ProductTemplate._meta.get_field(key).get_internal_type() in field_int:
                            try:
                                value = int(value)
                            except ValueError:
                                value = False
                        if value:
                            qtmpl[key] = value

        #price
        price = request.GET.get('price', False)
        if price:
            try:
                price = price.split(",")
                pf = int(price[0])
                pt = int(price[1])
                qprod['product_product_set__price__lte'] = pt
                qprod['product_product_set__price__gte'] = pf
            except:
                pass
        # #end search products by attributes
        return qtmpl, qprod

class ProductProduct(models.Model):
    """ProductProduct OpenERP"""
    __metaclass__ = TransMeta

    product_tmpl = models.ForeignKey('ProductTemplate', related_name='product_product_set')
    active = models.BooleanField(_('Active'), default=False)
    code = models.CharField(_('Code'), max_length=128, null=True) #Reference
    ean13 = models.CharField(_('EAN13'), max_length=128, null=True, blank=True)
    price = models.DecimalField(_('Price'), max_digits=9, decimal_places=2, default=0)
    price_special = models.DecimalField(_('Special Price'), max_digits=9, decimal_places=2, default=0, null=True, blank=True)
    attribute_group = models.CharField(_('Attribute Group'), max_length=128, null=True, blank=True)
    cartdescription = models.CharField(_('Cart Description'), max_length=256, blank=True)

    """ Custom fields model """

    class Meta:
        db_table = 'product_product'
        verbose_name = _('product')
        verbose_name_plural = _('products')
        translate = (
            'cartdescription',
        )
        ordering = ['-code']

    def __unicode__(self):
        return self.code

    def get_base_image(self):
        if self.product_images_set.filter(exclude = False, base_image = True).count() > 0:
            return self.product_images_set.filter(exclude = False, base_image = True)[0]
        else:
            return False

    def get_thumbnails(self):
        return self.product_images_set.filter(exclude = False, base_image = False)

    def get_all_images(self):
        return self.get_base_image(), self.get_thumbnails()

    def get_price(self):
        """ Get Price Product
        If special price != 0 and less than price, return special price.
        If not, return "normal" price
        """
        try:
            special_price = float(self.price_special)
        except:
            return self.price

        if special_price != 0.0 and special_price < self.price:
            price = special_price
        else:
            price = self.price

        return price

    @staticmethod
    def update_prices(request, product_ids):
        partner_id = request.user.get_profile().partner_id if request.user.user_profile_s.count() > 0 else False

        data = ''
        if partner_id:
            products = []
            for product in product_ids:
                try:
                    product = int(product)
                    products.append({'product_id':int(product),'quantity':1})
                except:
                    pass
            # values => {"1":{"regularPrice":"50"},"2":{"regularPrice":"100"}}
            values = conn_webservice('product.product','zoook_compute_price', [OERP_SALE, products, partner_id])
            data = json.dumps(values)
        return data

class ProductImages(models.Model):
    """ProductImages OpenERP"""

    name = models.CharField(_('Image Title'), max_length=128, null=True, blank=True)
    product = models.ForeignKey('ProductProduct', null=True, blank=True, related_name='product_images_set')
    filename = models.CharField(_('File Location'), max_length=128, null=True, blank=True)
    base_image = models.BooleanField(_('Base Image'), default=False)
    thumb_image = models.BooleanField(_('Thumb Image'), default=False)
    exclude = models.BooleanField(_('Exclude'), default=False)

    """ Custom fields model """

    class Meta:
        db_table = 'product_images'
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __unicode__(self):
        return self.name

class ProductHome(models.Model):
    """Product Home"""

    __metaclass__ = TransMeta

    tplproduct = models.ForeignKey(ProductTemplate)
    imgproduct = models.ImageField(_('image'), upload_to='catalog', blank=True, help_text=_("Check Documentation about size image"))
    description = models.TextField(_('description'), blank=True, null=True)
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text=_("Only items with their status set to 'Active' will be displayed."))
    order = models.IntegerField(_('order'),)

    class Meta:
        db_table = 'product_home'
        verbose_name = _('Product Home')
        verbose_name_plural = _('Products Home')
        translate = ('description', )
        ordering = ['order']

    def __unicode__(self):
        return self.tplproduct.name

class ProductRecommended(models.Model):
    """Product Recommended"""

    __metaclass__ = TransMeta

    tplproduct = models.ForeignKey(ProductTemplate)
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text=_("Only items with their status set to 'Active' will be displayed."))
    order = models.IntegerField(_('order'),)

    class Meta:
        db_table = 'product_recommended'
        verbose_name = _('Product Recommended')
        verbose_name_plural = _('Products Recommended')
        ordering = ['order']

    def __unicode__(self):
        return self.tplproduct.name

class ProductOffer(models.Model):
    """Product Offer"""

    __metaclass__ = TransMeta

    tplproduct = models.ForeignKey(ProductTemplate)
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_INACTIVE, help_text=_("Only items with their status set to 'Active' will be displayed."))
    order = models.IntegerField(_('order'),)

    class Meta:
        db_table = 'product_offer'
        verbose_name = _('Product Offer')
        verbose_name_plural = _('Products Offer')
        ordering = ['order']

    def __unicode__(self):
        return self.tplproduct.name

class ResManufacturer(models.Model):
    """Res Partner Manufacturer"""

    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=100, help_text=_("This is a unique identifier that allows your blogs to display its detail view, ex 'how-can-i-contribute'"), unique=True)
    active = models.BooleanField(_('Active'), default=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    logo  = models.ImageField(upload_to='manufacturer/', null=True, blank=True, help_text=_("Resize image. Check documentation about logo template"))

    class Meta:
        db_table = 'res_manufacturer'
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')
        translate = ('description',)

    def get_absolute_url(self):
        if LOCALE_URI:
            url = '/%s/%s/%s' % (get_language(), manufacturer_url[get_language()], self.slug)
        else:
            url = '/%s/%s' % (manufacturer_url[get_language()], self.slug)
        return url

    def __unicode__(self):
        return self.name

class ProductFields():
    """Product Fields Model"""

    @staticmethod
    def get_fields():
        """Get fields from ProductProduct and ProductTemplate. 
        Exclude some fields no using in attribute search
        Return tuple fields"""

        field_types = [
            'CharField',
            'BooleanField',
            'ForeignKey',
            'FloatField',
        ]

        prod_tpl_fields = []
        prod_fields = []

        prod_template_fields = ProductTemplate._meta.get_all_field_names()
        for field in prod_template_fields:
            try:
                if ProductTemplate._meta.get_field(field).get_internal_type() in field_types:
                    prod_tpl_fields.append(field)
            except:
                continue

        product_fields = ProductProduct._meta.get_all_field_names()
        for field in product_fields:
            if field[:2] == 'x_': #only fields start by x_ (product attribute)
                try:
                    if ProductProduct._meta.get_field(field).get_internal_type() in field_types:
                        prod_fields.append(field)
                except:
                    continue

        fields = prod_tpl_fields+prod_fields
        FIELDS = tuple([(item,item) for item in fields])
        
        return FIELDS

class AttributeSearch(models.Model):
    """Attribute Search"""

    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=64)
    categ = models.ManyToManyField('ProductCategory', null=True, blank=True, related_name='attribute_search_set', verbose_name=_('Categories'))
    price = models.BooleanField(_('Price'), default=True, help_text=_("Available Price Search"))
    active = models.BooleanField(_('Active'), default=True)
    default_box = models.BooleanField(_('Default'), default=False, help_text=_("Default Attribute Search Box. If you don't select some category, use this search box"))

    class Meta:
        db_table = 'attribute_search'
        verbose_name = _('Attribute Search')
        verbose_name_plural = _('Attributes Search')

    def __unicode__(self):
        return self.name

    def save(self):
        """
        Re-order all items at from 10 upwards, at intervals of 10.
        """
        super(AttributeSearch, self).save()

        current = 10
        for item in AttributeSearchItem.objects.filter(attribute=self).order_by('order'):
            item.order = current
            item.save()
            current += 10

class AttributeSearchItem(models.Model):
    """
    Attribute Search Items
    """
    __metaclass__ = TransMeta

    field = models.CharField(max_length=128, choices=ProductFields.get_fields())
    label = models.CharField(_('Cart Description'), max_length=128)
    attribute = models.ForeignKey(AttributeSearch)
    order = models.IntegerField(_('order'),)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        db_table = 'attribute_search_item'
        verbose_name = _('Attribute Search Item')
        verbose_name_plural = _('Attribute Search Items')
        translate = ('label', )
        ordering = ['order']

    def __unicode__(self):
        return "%s" % (self.field)

class AttributeSearchPrice(models.Model):
    """
    Attribute Search Prices
    """
    __metaclass__ = TransMeta

    pf = models.CharField(_('From'), max_length=64)
    pt = models.CharField(_('To'), max_length=64)
    attribute = models.ForeignKey(AttributeSearch)
    order = models.IntegerField(_('order'),)

    class Meta:
        db_table = 'attribute_search_price'
        verbose_name = _('Attribute Search Price')
        verbose_name_plural = _('Attribute Search Prices')
        ordering = ['order']

    def __unicode__(self):
        return "%s-%s" % (self.pf, self.pt)
