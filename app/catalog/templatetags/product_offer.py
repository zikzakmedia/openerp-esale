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

from django import template
from django.template import Library, Node

from zoook.catalog.models import ProductOffer, ProductProduct

register = template.Library()

class ProductOfferNode(Node):

    def render(self, context):
        products = ProductOffer.objects.filter(status=True)
        prods = []
        for recom in products:
            products = ProductProduct.objects.filter(product_tmpl=recom.tplproduct).order_by('price')
            base_image = products[0].get_base_image()

            prods.append({
                'template':recom.tplproduct,
                'products':products,
                'base_image':base_image,
                }
            )
        context['productitems'] = prods
        return ''

def productoffer(parser, token):
    """
    Product Offer:

    Basic tag Syntax::
        {% productoffer %}
    """

    return ProductOfferNode()

register.tag(productoffer)
