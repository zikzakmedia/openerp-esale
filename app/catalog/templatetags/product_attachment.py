# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2012 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
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

from zoook.base.models import IrAttachment

register = template.Library()

class ProductAttachmentNode(Node):
    def __init__(self, id, model, user):
        self.res_id = id
        self.res_model = model
        self.user = user

    def render(self, context):
        try:
            res_id = template.Variable(self.res_id).resolve(context)
            user = template.Variable(self.user).resolve(context)
        except:
            res_id = int(self.res_id)[1:-1]
            user = int(self.user)[1:-1]

        res_model = str(self.res_model)

        visibility = ['none']
        if not user:
            visibility.append('register')
        
        attachments = IrAttachment.objects.filter(res_id=res_id,res_model=res_model).exclude(visibility__in=visibility)

        context['attachmentitems'] = attachments
        return ''

def productattachment(parser, token):
    """
    Product Attachment:

    Basic tag Syntax::
        {% productattachment ID model %}
    """

    parts = token.split_contents()

    if len(parts) < 3:
        raise template.TemplateSyntaxError("'productattachment' tag must be of the form:  {% productattachment [ID] [model] [user] %}")

    return ProductAttachmentNode(parts[1], parts[2], parts[3])

register.tag(productattachment)
