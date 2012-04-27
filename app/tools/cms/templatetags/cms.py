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
from django.utils.translation import get_language, ugettext as _
from django.conf import settings

from settings import USER_ADD_APP, ADMIN_URI
from config import LOCALE_URI

import re

register = template.Library()

@register.inclusion_tag('cms/tags/user_add.html', takes_context = True)
def render_useradd(context):
    values = []

    sufix = ''
    if LOCALE_URI:
        sufix = "/%s" % (get_language())

    if 'user' in context:
        if hasattr(context['user'], 'has_perm'):
            for app_add in USER_ADD_APP:
                app  = app_add['app'].split('.')
                model_edit = '%s.add_%s' % (app[0],app[1])
                if context['user'].has_perm(model_edit):
                    values.append({
                            'url':'%s%s' % (sufix, app_add['url']),
                            'string':_(app_add['string']),
                        })

            #super admin
            if context['user'].is_staff:
                FILEBROWSER_URI = getattr(settings, "FILEBROWSER_URI", "/filebrowser/browse/")

                values.append({'url':FILEBROWSER_URI,'string':_('Media Files')})
                values.append({'url':ADMIN_URI,'string':_('Go to Admin')})

    return {
        'values': values,
    }

@register.filter
def split_metakey(value, arg=','):
    """Split arg by arg
    :param value str
    :param arg str
    :retun list
    """
    value = re.sub(' ','',value)
    return value.split(arg)

@register.filter
def replace(value, args=False):
    """Replace some characters 
    :param value str
    :param arg arguments separated by , (from, to)
    :retun str
    """
    if args is False:
        return value
    args = [arg.strip() for arg in args.split(',')]
    if not len(args)>1:
        return value
    return value.replace(args[0], args[1])

@register.simple_tag
def dictKeyLookup(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key, '')
