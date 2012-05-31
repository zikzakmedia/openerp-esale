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
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 900,
        'OPTIONS': {
            'MAX_ENTRIES': 500
        }
    }
}
LOCALE_PATHS = (
    '/home/resteve/django/zoook/locale',
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
OERP_SALES = [1,2] #Sale Shops. Orders by Sale Shops
OERP_COMPANY = 1 #Account Invoice. All invoices... use this Company ID.
COUNTRY_DEFAULT = 'ES'
PRODUCT_METADESCRIPTION = True
ATTACHMENT_SYNC = True
ATTACHMENT_SERVER = 'resteve@localhost'
ATTACHMENT_SERVER_PORT = '22'
ATTACHMENT_SSH_OPTION = ''
ATTACHMENT_RSYNC_OPTION = ''
ATTACHMENT_SOURCE = '/home/resteve/prova/openerp/'
ATTACHMENT_ROOT = '/home/resteve/prova/django/'

"""
Log's conf
"""
LOGFILE = '/home/resteve/django/zoook/log/sync.log' #path sync log
LOGSALE = '/home/resteve/django/zoook/log/sale.log' #path sale log

"""
Base template
"""
BASE_TEMPLATE = 'default'

"""
Url's conf
"""
LIVE_URL = "http://127.0.0.1:8000"
MEDIA_URL = "http://127.0.0.1:8000/static/"

"""
Database conf
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dj_zoook',     # Or path to database file if using sqlite3.
        'USER': 'openerp',      # Not used with sqlite3.
        'PASSWORD': 'openerp',  # Not used with sqlite3.
        'HOST': 'localhost',    # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '5432',         # Set to empty string for default. Not used with sqlite3.
        'PORT': '5433',
    }
}

"""
OpenERP Webservice Connection
"""
OERP_CONF = {
    'username':'admin',
    'password':'admin',
    'dbname':'oerp6_zoook',
    'protocol':'xmlrpc', #xmlrpc
    'uri':'http://localhost', #xmlrpc
    'port':8051, #xmlrpc
#    'protocol':'pyro', #pyro
#    'uri':'localhost', #pyro
#    'port':8071, #pyro
}

PROJECT_APPS = (
    'blog',
    'south',
    #'sermepa.sermepa',
    #'sermepa.sermepa_test',
    #'payment.sermepa',
    #'paypal.standard.ipn',
    #'payment.paypal',
    #'pasat4b.pasat4b',
    #'payment.pasat4b',
    #'payment.check',
    #'payment.cashondelivery',
    #'payment.debit',
)

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
PROJECT_USER_ADD_APP = [
    {'app':'blog.blog','url':'/blog/add/','string':'Add Blog'},
    {'app':'catalog.producthome','url':'/catalogmanage/producthome/','string':'Prod. Home'},
    {'app':'catalog.productrecommended','url':'/catalogmanage/productrecommended/','string':'Prod. Recommended'},
    {'app':'catalog.productoffer','url':'/catalogmanage/productoffer/','string':'Prod. Offer'},
]

"""
Project locale independent paths
"""
PROJECT_LOCALE_INDEPENDENT_PATHS  = ()

"""
Email conf
"""
EMAIL_HOST = 'smtp.gmail.com'
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
Paypal Configuration
"""
PAYPAL_RECEIVER_EMAIL = ""
PAYPAL_CURRENCY = 'EUR'

"""
Sermepa/Servired Configuration
"""
SERMEPA_URL_PRO = 'https://sis.sermepa.es/sis/realizarPago'
SERMEPA_URL_TEST = 'https://sis-t.sermepa.es:25443/sis/realizarPago'
SERMEPA_MERCHANT_URL = "http://127.0.0.1:8000/payment/sermepa/ipn"
SERMEPA_MERCHANT_NAME = "Zikzakmedia SL"
SERMEPA_MERCHANT_CODE = ''
SERMEPA_SECRET_KEY = ''
SERMEPA_BUTTON_IMG = '/static/images/icons/sermepa.png'
SERMEPA_TERMINAL = 1
SERMEPA_CURRENCY = 978
SERMEPA_TRANS_TYPE = 0 # 0 - Autorizacion / 1 - Preautorizacion / 2 - Confirmacion / 3 - Devolución Automatica / 4 - Pago Referencia / 5 - Transacción Recurrente / 6 - Transacción Sucesiva / 7 - Autenticación / 8 - Confirmación de Autenticación / 9 - Anulacion de Preautorizacion

"""
Passat 4b Configuration
"""
PASAT4B_MERCHANT_CODE = 'PI00000000'
PASAT4B_BUTTON_IMG = '/static/images/icons/passat4b.png'
PASAT4B_BUTTON_TEXT = 'Comprar ahora'
PASAT4B_DECIMAL = 2

"""
Twitter
"""
TWITTER_USER = 'zoook_esale'
