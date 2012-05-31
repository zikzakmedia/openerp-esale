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

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from settings import *
from tools.conn import conn_webservice
from tools.zoook import siteConfiguration, checkPartnerID, checkFullName, connOOOP, paginationOOOP

from sale.models import *
from catalog.models import ProductProduct, ProductTemplate
from base.models import * 

import datetime
import time
import re
import logging

_('draft')
_('waiting_date')
_('manual')
_('progress')
_('shipping_except')
_('invoice_except')
_('done')
_('cancel')

@login_required
def orders(request):
    """
    Orders. All Orders Partner Available
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = {}
    total = len(conn.SaleOrder.filter(partner_id=partner_id, shop_id__in=OERP_SALES))
    offset, page_previous, page_next = paginationOOOP(request, total, PAGINATOR_ORDER_TOTAL)

    values = conn.SaleOrder.filter(partner_id=partner_id, shop_id__in=OERP_SALES, offset=offset, limit=PAGINATOR_ORDER_TOTAL, order='date_order DESC, name DESC')

    title = _('All Orders')
    metadescription = _('List all orders of %s') % full_name

    return render_to_response("sale/orders.html", {
                'title':title,
                'metadescription':metadescription,
                'values':values,
                'page_previous':page_previous,
                'page_next':page_next,
            }, context_instance=RequestContext(request))

@login_required
def order(request, order):
    """
    Order. Order Detail Partner
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order, shop_id__in=OERP_SALES)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]
    title = _('Order %s') % (value.name)
    metadescription = _('Details order %s') % (value.name)
    currency = value.pricelist_id.currency_id.symbol
        
    return render_to_response("sale/order.html", {
                'title': title,
                'metadescription': metadescription,
                'value': value,
                'currency': currency,
            }, context_instance=RequestContext(request))

@login_required
def cancel(request, order):
    """
    Order. Cancel Order
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order, shop_id__in=OERP_SALES)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]

    if value.state != 'draft':
        error = _('Your order is in progress and it is not possible to cancel. Contact with us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    #cancel order
    try:
        cancel = conn_webservice('sale.order','action_cancel', [[value.id]])
    except:
        error = _('An error is getting when cancel this order. Try again or contact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    #drop session if exists
    if 'sale_order' in request.session:
        if request.session['sale_order'] == value.name:
            del request.session['sale_order']

    value = conn.SaleOrder.get(value.id) #reload sale order values
    title = _('Order %s cancelled') % (value.name)
    metadescription = _('Order %s cancelled') % (value.name)

    return render_to_response("sale/order.html", {
                'title': title,
                'metadescription': metadescription,
                'value': value,
            }, context_instance=RequestContext(request))

@login_required
def payment(request, order):
    """
    Payment. Payment Order
    """

    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.SaleOrder.filter(partner_id=partner_id, name=order, shop_id__in=OERP_SALES)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]

    if value.state != 'draft' or value.payment_state != 'draft':
        error = _('Your order is in progress or this order was payed')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    sale_shop = conn.SaleShop.filter(id=OERP_SALE)[0]
    payments = sale_shop.zoook_payment_types
    
    title = _('Payment Order %s') % (value.name)
    metadescription = _('Payment Order %s') % (value.name)
    currency = value.pricelist_id.currency_id.symbol

    return render_to_response("sale/payment.html", {
                'title': title, 
                'metadescription': metadescription, 
                'value': value, 
                'payments': payments, 
                'currency': currency,
            }, context_instance=RequestContext(request))

def check_order(conn, partner_id, OERP_SALE):
    """
    Check Order
    Check order if available a order draft state, draft payment_state and same Shop ID
    """

    orders = conn.SaleOrder.filter(partner_id=partner_id, state='draft', payment_state ='draft', shop_id=OERP_SALE)

    # get a draft order
    if len(orders)>0:
        order = orders[0]
    # new order
    else:
        partner = conn.ResPartner.get(partner_id)
        partner_addresses = conn.ResPartnerAddress.filter(partner_id=partner_id)
        address = {}
        for partner_address in partner_addresses:
            if partner_address.type == 'delivery':
                address['delivery'] = partner_address
            if partner_address.type == 'invoice':
                address['invoice'] = partner_address
            if partner_address.type == 'contact':
                address['contact'] = partner_address
       
        if len(address) > 0:
            if not 'delivery' in address:
                address['delivery'] = partner_addresses[0]
            if not 'invoice' in address:
                address['invoice'] = partner_addresses[0]
            if not 'contact' in address:
                address['contact'] = partner_addresses[0]
            
            #create new order
            shop = conn.SaleShop.get(OERP_SALE)
            order = conn.SaleOrder.new()
            order.shop_id = shop
            order.date_order = datetime.date.today() # not time.strftime('%Y-%m-%d')
            order.partner_id = partner
            order.partner_invoice_id = address['invoice']
            order.partner_order_id = address['contact']
            order.partner_shipping_id = address['delivery']
            order.picking_policy = 'one'
            order.pricelist_id = partner.property_product_pricelist and partner.property_product_pricelist or shop.pricelist_id
            order.save()
        else:
            order = 'error'

    return order

def check_product(conn, code):
    """
    Check Product
    """

    #check if this product exist
    product = False
    products = ProductProduct.objects.filter(code=code)
    if len(products)> 0:
        product = products[0]

    return product

@login_required
def checkout(request):
    """
    Checkout. Order Cart
    """

    context_instance=RequestContext(request)

    if 'sale_order' in request.session:
        return HttpResponseRedirect("%s/sale/order/%s" % (context_instance['LOCALE_URI'],request.session['sale_order']))

    site_configuration = siteConfiguration(SITE_ID)

    message = False
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    order = check_order(conn, partner_id, OERP_SALE)
    
    if order == 'error':
        return HttpResponseRedirect("%s/partner/partner/" % (context_instance['LOCALE_URI']))

    if request.method == 'POST':
        qty = int(request.POST['qty'])
        code = request.POST['code']
        #check product is available to add to cart
        product = check_product(conn, code)
        if product:
            #check if this product exist
            product_line = conn.SaleOrderLine.filter(order_id=order.id, product_id=product.id)
            product = conn.ProductProduct.get(product.id)
            partner = conn.ResPartner.get(partner_id)

            if len(product_line) > 0: #product line exist -> update
                order_line = conn.SaleOrderLine.get(product_line[0].id)
                order_line.product_uom_qty = qty+product_line[0].product_uom_qty
                order_line.save()
            else: #product line not exist -> create
                if partner.property_product_pricelist:
                    pricelist = partner.property_product_pricelist.id
                else:
                    shop = conn.SaleShop.get(OERP_SALE)
                    pricelist = shop.pricelist_id.id
                values = [
                    [order.id], #ids
                    pricelist, #pricelist
                    product.id, #product
                    qty, #qty
                    False, #uom
                    0, #qty_uos
                    False, #uos
                    '', #name
                    partner_id, #partner_id
                ]
                product_id_change = conn_webservice('sale.order.line','product_id_change', values)

                sale_order_add_product = True
                if product_id_change['warning'] and SALE_ORDER_PRODUCT_CHECK:
                    not_enought_stock = _('Not enough stock !')
                    sale_order_add_product = False

                if sale_order_add_product:
                    product_value = product_id_change['value']
                    order_line = conn.SaleOrderLine.new()
                    order_line.order_id = order
                    order_line.name = product_id_change['value']['name']
                    if 'notes' in product_value:
                        order_line.notes = product_id_change['value']['notes']
                    order_line.product_id = product
                    order_line.product_uom_qty = qty
                    order_line.product_uom = product.product_tmpl_id.uom_id
                    order_line.delay = product_id_change['value']['delay']
                    order_line.th_weight = product_id_change['value']['th_weight']
                    order_line.type = product_id_change['value']['type']
                    order_line.price_unit = product_id_change['value']['price_unit']
                    order_line.purchase_price = product_id_change['value']['purchase_price']
                    order_line.tax_id = [conn.AccountTax.get(t_id) for t_id in product_id_change['value']['tax_id']]
                    order_line.product_packaging = ''
                    order_line.save()
                else:
                    message = product_id_change['warning']

                if message and 'title' in message:
                    message = message['title']

            #recalcule order (refresh amount)
            order = check_order(conn, partner_id, OERP_SALE)

    #list order lines
    lines = conn.SaleOrderLine.filter(order_id=order.id)

    title = _('Checkout')
    metadescription = _('Checkout order %s') % (site_configuration.site_title)
    
    values = {
        'title': title,
        'metadescription': metadescription,
        'message':message,
        'order':order,
        'lines': lines,
    }

    if len(lines)>0:
        #delivery
        try:
            values['deliveries'] = conn_webservice('sale.order','delivery_cost', [order.id])
            delivery = True
        except:
            logging.basicConfig(filename=LOGFILE,level=logging.INFO)
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Need configure grid delivery in this shop or delivery grid not available'))
            values['deliveries'] = []
            
        #Address invoice/delivery
        values['address_invoices'] = conn.ResPartnerAddress.filter(partner_id=partner_id,type='invoice')
        values['address_deliveries'] = conn.ResPartnerAddress.filter(partner_id=partner_id,type='delivery')
        sale_shop = conn.SaleShop.filter(id=OERP_SALE)[0]

        #order payment by sequence
        payments = []
        if sale_shop.zoook_payment_types:
            payment_commission = False
            for payment_type in sale_shop.zoook_payment_types:
                if payment_type.commission:
                    payment_commission = True
                payments.append({'sequence':payment_type.sequence,'app_payment':payment_type.app_payment,'name':payment_type.payment_type_id.name})
            #if payment commission is available, recalculate extra price
            if payment_commission:
                payments = conn_webservice('zoook.sale.shop.payment.type','get_payment_commission', [order.id])
        else:
            logging.basicConfig(filename=LOGFILE,level=logging.INFO)
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Need configure payment available in this shop'))

        values['payments'] = sorted(payments, key=lambda k: k['sequence']) 

    values['countries'] = ResCountry.objects.all()
    values['country_default'] = COUNTRY_DEFAULT

    return render_to_response("sale/checkout.html", values, context_instance=RequestContext(request))

@login_required
def checkout_remove(request, code):
    """
    Checkout. Order cart
    """
    
    context_instance=RequestContext(request)

    products = ProductProduct.objects.filter(code=code)
    if len(products) > 0:
        partner_id = checkPartnerID(request)
        if not partner_id:
            error = _('Are you a customer? Please, contact us. We will create a new role')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        full_name = checkFullName(request)
        conn = connOOOP()
        if not conn:
            error = _('Error when connecting with our ERP. Try again or cantact us')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
        order = check_order(conn, partner_id, OERP_SALE)
        order_lines = conn.SaleOrderLine.filter(order.id, product_id=products[0].id)
        if len(order_lines) > 0:
            order_line = conn.SaleOrderLine.get(order_lines[0].id)
            order_line.delete()

    return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

@login_required
def checkout_confirm(request):
    """
    Checkout. Confirm
    """

    logging.basicConfig(filename=LOGSALE,level=logging.INFO)
    context_instance=RequestContext(request)

    if 'sale_order' in request.session:
        return HttpResponseRedirect("%s/sale/order/%s" % (context_instance['LOCALE_URI'],request.session['sale_order']))

    if request.method == 'POST':
        partner_id = checkPartnerID(request)
        if not partner_id:
            error = _('Are you a customer? Please, contact us. We will create a new role')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

        full_name = checkFullName(request)

        conn = connOOOP()
        if not conn:
            error = _('Error when connecting with our ERP. Try again or cantact us')
            return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
            
        partner = conn.ResPartner.get(partner_id)
        order = check_order(conn, partner_id, OERP_SALE)

        if order.state != 'draft':
            return HttpResponseRedirect("%s/sale/" % (context_instance['LOCALE_URI']))

        delivery = request.POST.get('delivery') and request.POST.get('delivery') or False
        payment = request.POST['payment'] and request.POST['payment'] or False
        address_invoice = request.POST['address_invoice'] and request.POST['address_invoice'] or False
        address_delivery = request.POST['address_delivery'] and request.POST['address_delivery'] or False

        #delivery
        if delivery:
            delivery = delivery.split('|')
            carrier = conn.DeliveryCarrier.filter(code=delivery[0])
            if len(carrier) == 0:
                return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))
            carrier = carrier[0]

            if partner.property_product_pricelist:
                pricelist = partner.property_product_pricelist.id
            else:
                shop = conn.SaleShop.get(OERP_SALE)
                pricelist = shop.pricelist_id.id

            values = [
                [order.id], #ids
                pricelist, #pricelist
                carrier.product_id.id, #product
                1, #qty
                False, #uom
                0, #qty_uos
                False, #uos
                '', #name
                partner.id, #partner_id
            ]

            product_id_change = conn_webservice('sale.order.line','product_id_change', values)
            order_line = conn.SaleOrderLine.new()
            order_line.order_id = order
            order_line.name = carrier.product_id.name
            order_line.product_id = carrier.product_id
            order_line.product_uom_qty = 1
            order_line.product_uom = carrier.product_id.product_tmpl_id.uom_id
            order_line.delay = product_id_change['value']['delay']
            order_line.th_weight = product_id_change['value']['th_weight']
            order_line.type = product_id_change['value']['type']
            order_line.price_unit = float(re.sub(',','.',delivery[1]))
            order_line.tax_id = [conn.AccountTax.get(t_id) for t_id in product_id_change['value']['tax_id']]
            order_line.product_packaging = ''
            order_line.save()

            #delivery
            order.carrier_id = carrier

        #payment type
        payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment=payment)
        if len(payment_type) > 0:
            if payment_type[0].commission: #add new order line
                payment = conn_webservice('zoook.sale.shop.payment.type','set_payment_commission', [order.id, payment])
            order.payment_type = payment_type[0].payment_type_id
            order.picking_policy = payment_type[0].picking_policy
            order.order_policy = payment_type[0].order_policy
            order.invoice_quantity = payment_type[0].invoice_quantity
        else:
            return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

        #Replace invoice address and delivery address
        if address_invoice:
            #add new invoice address
            if address_invoice == 'add_invoice':
                address = conn.ResPartnerAddress.new()
                address.name = request.POST['invoice_name']
                address.partner_id = conn.ResPartner.get(partner_id)
                address.type = 'invoice'
                address.street = request.POST['invoice_street']
                address.zip = request.POST['invoice_zip']
                address.city = request.POST['invoice_city']
                countries = ResCountry.objects.filter(code=request.POST['invoice_country_code'])
                if len(countries)>0:
                    country = countries[0].id
                    address.country_id = conn.ResCountry.get(country)
                if request.user.email:
                    address.email = request.user.email
                address.phone = request.POST['invoice_phone']
                address_invoice = address.save()

            address_invoice = conn.ResPartnerAddress.get(int(address_invoice))
            if address_invoice:
                order.partner_invoice_id = address_invoice
        else:
            return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

        if address_delivery:
            #add new delivery address
            if address_delivery == 'add_delivery':
                address = conn.ResPartnerAddress.new()
                address.name = request.POST['delivery_name']
                address.partner_id = conn.ResPartner.get(partner_id)
                address.type = 'delivery'
                address.street = request.POST['delivery_street']
                address.zip = request.POST['delivery_zip']
                address.city = request.POST['delivery_city']
                countries = ResCountry.objects.filter(code=request.POST['delivery_country_code'])
                if len(countries)>0:
                    country = countries[0].id
                    address.country_id = conn.ResCountry.get(country)
                if request.user.email:
                    address.email = request.user.email
                address.phone = request.POST['delivery_phone']
                address_delivery = address.save()

            address_delivery = conn.ResPartnerAddress.get(int(address_delivery))
            if address_delivery:
                order.partner_shipping_id = address_delivery
        else:
            return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

        #cupon code / promotion
        code_promotion = request.POST['promotion']
        if code_promotion:
            order.coupon_code = code_promotion

        #payment state
        order.payment_state = 'checking'
        order.save()

        #apply cupon code / promotion
        if code_promotion:
            promotion = conn_webservice('promos.rules','apply_promotions', [order.id])
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Apply promotion %s Order %s' % (code_promotion, order.name) ))

        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Payment %s Order %s' % (payment_type[0].app_payment, order.name) ))

        request.session['sale_order'] = order.name

        return HttpResponseRedirect("%s/payment/%s/" % (context_instance['LOCALE_URI'], payment_type[0].app_payment))
    else:
        return HttpResponseRedirect("%s/sale/checkout/" % (context_instance['LOCALE_URI']))

def checkout_payment(request):
    """
    Redirect Payment App from Sale Order (My Account)
    """

    context_instance=RequestContext(request)
    payment = request.POST.get('payment', '')
    order = request.POST.get('order', '')

    conn = connOOOP()
    payment_type = conn.ZoookSaleShopPaymentType.filter(app_payment=payment)

    order = conn.SaleOrder.filter(name=order,state='draft',payment_state='draft')

    if (len(payment_type) > 0) and (len(order) > 0):
        request.session['sale_order'] = order[0].name
        return HttpResponseRedirect("%s/payment/%s/" % (context_instance['LOCALE_URI'], payment_type[0].app_payment))
    else:
        error = _('This payment is not available. Use navigation menus')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

def payorder(request):
    """
    Payment Order without login
    Only Pay Order when:
      - State Draft 
      - Payment State Draft
      - Shop ID
    """

    name = request.GET.get('name', '')
    total = request.GET.get('total', '')
    
    title = _('Payment Order by reference')
    metadescription = _('Payment Order by reference')

    message = False
    value = False
    payments = False
    currency = DEFAULT_CURRENCY

    if request.method == 'POST':
        form = PayorderForm(request.POST)
        if form.is_valid():
            conn = connOOOP()
            if not conn:
                error = _('Error when connecting with our ERP. Try again or cantact us')
                return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

            name = form.cleaned_data['name']
            total = float(form.cleaned_data['total'])

            values = conn.SaleOrder.filter(name=name, amount_total=total, state='draft', payment_state ='draft', shop_id__in=OERP_SALES)

            if len(values)>0:
                value = values[0]
                title = _('Order %s') % (value.name)
                metadescription = _('Details order %s') % (value.name)
                sale_shop = conn.SaleShop.filter(id=OERP_SALE)[0]
                payments = sale_shop.zoook_payment_types
                currency = value.pricelist_id.currency_id.symbol
            else:
                message = _('Try again. There are not some reference pending to pay or total do not match.')
        else:
            message = _('Try again. Insert reference and total Order.')

    return render_to_response("sale/payorder.html", {
            'title': title,
            'metadescription': metadescription,
            'name': name,
            'total': total,
            'message': message,
            'value': value,
            'payments': payments,
            'currency': currency,
        }, context_instance=RequestContext(request))
