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

from catalog.models import ResManufacturer

register = template.Library()

class ManufacturersNode(Node):
    def render(self, context):
        context['manufacturers'] = ResManufacturer.objects.filter(active=True).order_by('name')

        return ''

def manufacturers(parser, token):
    """
    Manufacturers:

    Basic tag Syntax::
        {% manufacturers %}
    """

    return ManufacturersNode()

register.tag(manufacturers)
