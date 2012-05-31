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

from catalog.models import ProductCategory
from django.utils.translation import get_language
from config import LOCALE_URI

register = template.Library()

def render_category_menu(context):
    root_category = ProductCategory.objects.filter(parent=None)

    oldlevel = 0
    values = []
    if root_category.count() > 0:
        categories = root_category[0].collect_children(level=1, children = [])

        for (category, level) in categories:
            values.append((ProductCategory.objects.get(id=category), level, oldlevel))
            oldlevel = level

    return {
        'values': values,
        'lastlevel': oldlevel,
        'LOCALE_URI': context['LOCALE_URI'],
    }

@register.inclusion_tag('catalog/tags/horizontal_menu.html', takes_context = True)
def render_horizontal_menu(context):
    """Render category tree (all categories and childs) to horizontal menu.
    Horizontal Menu only suport 5 levels"""
    return render_category_menu(context)

@register.inclusion_tag('catalog/tags/vertical_menu.html', takes_context = True)
def render_vertical_menu(context):
    """Render category tree (all categories and childs) to vertical menu."""
    return render_category_menu(context)
