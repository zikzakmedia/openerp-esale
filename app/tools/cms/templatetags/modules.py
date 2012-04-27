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
from zoook.tools.cms.models import Modules

register = template.Library()

class ModuleNode(Node):
    def __init__(self, position):
        self.position = position
 
    def render(self, context):
        entry = ''
        entries = Modules.objects.filter(position=self.position,status=True)
        if entries:
            entry = entries[0].description

        return entry

def module(parser, token):
    """
    Show Module data CMS:

    Basic tag Syntax::
        {% module [position]%}

    *position* Key ID position Module

    Demo:
      {% module catalog.right %}
    """

    parts = token.split_contents()

    if len(parts) < 1:
        raise template.TemplateSyntaxError("'module' tag must be of the form:  {% module identification%}")

    return ModuleNode(parts[1])

register.tag(module)
