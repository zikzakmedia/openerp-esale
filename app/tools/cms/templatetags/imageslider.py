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
from zoook.tools.cms.models import ImageSlider, ImageSliderItem

register = template.Library()

class SliderNode(Node):
    def __init__(self, slug):
        self.slug = slug
 
    def render(self, context):
        slideritems = []
        slider = ImageSlider.objects.filter(slug=self.slug)

        if len(slider)>0:
            j = 0
            for i in ImageSliderItem.objects.filter(slider=slider[0],status=True).order_by('order'):
                j = j+1
                slideritems.append({'position':j,'slimg':i.slimg,'title':i.title,'url':i.link_url})

        context['slideritems'] = slideritems
        return ''

def imageslider(parser, token):
    """
    Image Slider:

    Basic tag Syntax::
        {% imageslider [slug]%}

    *slug* Key ID slug ImageSlider

    Demo:
      {% imageslider topproducts %}{% for item in slideritems %}{{ item.title }}{% endfor %}
    """

    parts = token.split_contents()

    if len(parts) < 1:
        raise template.TemplateSyntaxError("'imageslider' tag must be of the form:  {% imageslider identification%}")

    return SliderNode(parts[1])

register.tag(imageslider)
