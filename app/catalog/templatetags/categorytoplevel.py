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
from django.utils.translation import get_language

from zoook.catalog.models import ProductCategory

register = template.Library()

class CategoryToplevelNode(Node):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        try:
            slug = template.Variable(self.slug).resolve(context)
        except:
            slug = str(self.slug)[1:-1]

        kwargs = {
            'status': True,
        }

        if self.slug:
            kwargs['slug_'+get_language()] = slug #filter category slug
        else:
            kwargs['parent'] = None #top category

        top = ProductCategory.objects.filter(**kwargs)

        if len(top)>0:
            categories = ProductCategory.objects.filter(parent=top[0],status=True).order_by('position')
            context['toplevel'] = categories
        else:
            context['toplevel'] = []
        return ''

def categorytoplevel(parser, token):
    """
    Category Top Level:

    Basic tag Syntax::
        {% categorytoplevel [slug] %}
    """
    parts = token.split_contents()

    slug = None
    if len(parts) > 1:
        slug = parts[1]

    return CategoryToplevelNode(slug)

register.tag(categorytoplevel)
