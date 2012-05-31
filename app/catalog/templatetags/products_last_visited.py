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

from zoook.catalog.models import ProductTemplate, ProductProduct

register = template.Library()

class ProductsLastVisitedNode(Node):
    def __init__(self, num = 5):
        self.num = num

    def render(self, context):
        prods = []
        request = context['request']
        products_last_visited = request.session.get('last_visited', [])
        products_last_visited = products_last_visited[-int(self.num):]
        templates = ProductTemplate.objects.filter(id__in=products_last_visited)

        for template in templates:
            products = ProductProduct.objects.filter(product_tmpl=template).order_by('price')
            base_image = products[0].get_base_image()

            prods.append({
                'template':template,
                'products':products,
                'base_image':base_image,
                }
            )

        context['productitems'] = prods
        return ''

def productslastvisited(parser, token):
    """
    Products Last Visited:

    Basic tag Syntax::
        {% catalog_last_visited [num] %}
    """

    num = 5
    parts = token.split_contents()

    if len(parts) > 1:
        num = parts[1]

    return ProductsLastVisitedNode(num)

register.tag(productslastvisited)
