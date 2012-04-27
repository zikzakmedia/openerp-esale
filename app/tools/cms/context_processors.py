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

from django.utils.translation import get_language

from tools.zoook import siteConfiguration

from settings import BASE_TEMPLATE, LIVE_URL
from config import LOCALE_URI, SITE_ID

def theme(request):
    """
    Params context template:
     - SITE_TITLE: Site name (title html pages)
     - THEME: name template teme
    Return dicc
    """

    site_configuration = siteConfiguration(SITE_ID)

    return {
        'SITE_TITLE': site_configuration.site_title,
        'THEME': BASE_TEMPLATE,
    }

def site_configuration(request):
    """
    Get Site Configuration values
    :SITE_CONF:  Object Site Configuration
    :LIVE_URL: Str URL Site
    :LOCALE_URI: Available locale uri
    Return dicc
    """

    site_configuration = siteConfiguration(SITE_ID)

    sufix = ''
    if LOCALE_URI:
        sufix = "/%s" % get_language()

    user_name = False
    full_name = False
    if request.user.is_active:
        user_name = request.user
        full_name = request.user.get_full_name()
        if not full_name:
            full_name = user_name

    return {
        'SITE_CONF': site_configuration,
        'SITE_URI': LIVE_URL,
        'LOCALE_URI': sufix,
        'USER_NAME': user_name,
        'FULL_NAME': full_name,
    }
