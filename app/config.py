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

from django.utils.translation import ugettext_lazy as _

import re

DEBUG = True
MAINTENANCE_MODE = False
ROOT_URLCONF = 'zoook.urls'
ADMIN_URI = '/manager/'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '',
        'TIMEOUT': 900,
        'OPTIONS': {
            'MAX_ENTRIES': 500
        }
    }
}
LOCALE_PATHS = (
    '',
)

"""
Site Django
"""
SITE_ID = 1

"""
Localization and locale
"""
TIME_ZONE = 'Europe/Madrid'

ugettext = lambda s: s

#Edit your languages
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
)
DEFAULT_LANGUAGE = 1
LOCALE_URI = True
LOCALEURL_USE_ACCEPT_LANGUAGE = True
LOCALES =  {
    'en':'en_US',
    'es':'es_ES',
}

"""
Default Currency Sale Shop
"""
DEFAULT_CURRENCY = '€'

"""
Sale Order, when add product, continue if get warning
True: If get warning, not add product
False: If get warning, add product
"""
SALE_ORDER_PRODUCT_CHECK = True

"""
OpenERP Conf
"""
OERP_SALE = 1 #Sale Shop. All price, orders, ... use this Sale Shop ID.
OERP_SALES = [1] #Sale Shops. Orders by Sale Shops
OERP_COMPANY = 1 #Account Invoice. All invoices... use this Company ID.
COUNTRY_DEFAULT = 'ES'
PRODUCT_METADESCRIPTION = True

"""
Log's conf
"""
LOGFILE = '' #path sync log
LOGSALE = '' #path sale log

"""
Base template
"""
BASE_TEMPLATE = 'default'

"""
Url's conf
"""
LIVE_URL = ""
MEDIA_URL = ""

"""
Database conf
"""
DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',     # Or path to database file if using sqlite3.
        'USER': '',      # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',         # Set to empty string for default. Not used with sqlite3.
    }
}

"""
OpenERP Webservice Connection
"""
OERP_CONF = {
    'username':'',
    'password':'',
    'dbname':'',
    'protocol':'', #xmlrpc
    'uri':'', #xmlrpc
    'port':, #xmlrpc
}

PROJECT_APPS = ()

"""
Pagination values
"""
PAGINATION_DEFAULT_TOTAL = 9
PAGINATOR_ITEMS = [9,18,36]
PAGINATOR_ORDER_TOTAL = 5 #remember change this value in your order template
PAGINATOR_INVOICE_TOTAL = 5 #remember change this value in your invoice template
PAGINATOR_BLOG_TOTAL = 5 #remember change this value in your blog template
PAGINATOR_MANUFACTURER_TOTAL = 49

"""
Project User Add APP
"""
PROJECT_USER_ADD_APP = []

"""
Project locale independent paths
"""
PROJECT_LOCALE_INDEPENDENT_PATHS  = ()

"""
Email conf
"""
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_FROM = ''
EMAIL_REPPLY = ''

"""
Recaptcha keys
"""
RECAPTCHA_PUB_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

"""
Twitter
"""
TWITTER_USER = 'zoook_esale'
