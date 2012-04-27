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

from catalog.models import ProductCategory, ProductTemplate, ProductProduct, AttributeSearch, AttributeSearchItem, AttributeSearchPrice
from django.utils.translation import get_language
from config import DEFAULT_CURRENCY

register = template.Library()

@register.inclusion_tag('catalog/tags/attribute_form.html', takes_context = True)
def attribute_form(context, category):
    """
    Get Items in Attribute Search for design Search Form
    - Get Attribute Search available in this category
    - Get all items in this Attribute Search (name, type, options)
    return {'fields','path_info'}
    """

    literals = {'None': None, 'False': False, 'True': True}
    if category in literals:
        category = literals[category]

    if category:
        #category
        kwargs = {
            'slug_'+get_language(): category, #slug is unique
            'status': True,
        }
        categories = ProductCategory.objects.filter(**kwargs)
        category = categories[0]

    #attribute box
    attributes = AttributeSearch.objects.filter(active=True,categ=category)
    if attributes.count() == 0: #use default attribute box
        attributes = AttributeSearch.objects.filter(active=True,default_box=True)
        if attributes.count() == 0: #there are not default attribute box
            return {'fields': []}

    #fields attributes search
    fields = []
    for item in AttributeSearchItem.objects.filter(active=True,attribute=attributes[0]).order_by('order'):
        """
        Product Product start by x_
            type
            options (selected field/CharField)
        Product Template
            type
            options (ForeignKey)
            options (selected field/CharField)
        """
        if item.field[:2] == 'x_':
            try:
                type = ProductProduct._meta.get_field(item.field).get_internal_type()
            except:
                type = "CharField"
            options = ProductProduct._meta.get_field(item.field).choices
        else:
            try:
                type = ProductTemplate._meta.get_field(item.field).get_internal_type()
            except:
                type = "CharField"
            if type == 'ForeignKey':
                opts = []
                obj_rel = ProductTemplate._meta.get_field(item.field).rel.to
                for i in obj_rel.objects.filter(active=True).order_by('name'):
                    opts.append((str(i.id),i.name))
                options = tuple(opts)
            else:
                options = ProductTemplate._meta.get_field(item.field).choices

        if len(options) > 0:
            type = "SelectionField" #change field type CharField to SelectionField

        default = ''
        if item.field in context['request'].GET:
            default = context['request'].GET[item.field]

        fields.append({
            'name': item.field,
            'label': item.label,
            'options': options,
            'type': type,
            'default': default,
        })

    path_info = context['request'].META['PATH_INFO']

    #price
    price = False
    price_options = []
    if attributes[0].price:
        price = True
        for p in AttributeSearchPrice.objects.filter(attribute=attributes[0]).order_by('order'):
            price_options.append([p.pf,p.pt])
    price_default = ''
    if 'price' in context['request'].GET:
        try:
            price_default = str(context['request'].GET['price'].split(',')[0])
        except:
            pass

    # return dicc
    return {
        'fields': fields,
        'path_info': path_info,
        'price': price,
        'price_options': price_options,
        'price_default': price_default,
        'currency': DEFAULT_CURRENCY,
    }
