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

from django.conf.urls.defaults import *

"""Urls Sale"""

urlpatterns = patterns("",
    url(r'^$', 'sale.views.orders', name='sale'),
    url(r'^cancel/(?P<order>[^/]+)$', 'sale.views.cancel', name='sale_cancel'),
    url(r"^payorder/", 'sale.views.payorder', name='payment_order'),
    url(r'^payment/(?P<order>[^/]+)$', 'sale.views.payment', name='sale_payment'),
    url(r"^order/(?P<order>[^/]+)$", 'sale.views.order', name='sale_order'),
    url(r"^checkout/remove/(?P<code>[^/]+)$", 'sale.views.checkout_remove', name='sale_checkout_remove'),
    url(r"^checkout/confirm/", 'sale.views.checkout_confirm', name='sale_checkout_confirm'),
    url(r"^checkout/payment/", 'sale.views.checkout_payment', name='sale_checkout_payment'),
    url(r"^checkout/", 'sale.views.checkout', name='sale_checkout'),
)
