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

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib.sitemaps import GenericSitemap

from views import index
from settings import MEDIA_ROOT
from sitemaps import sitemaps
from transurl import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('django.conf',
                 'django.contrib.admin',
                ),
}

urlpatterns = patterns('',
    url(r"^$", index, name='index'),

    # catalog 
    url(r"^%s/" % catalog_url['en'], include("catalog.urlsCatalog")),
    url(r"^%s/"% catalog_url['es'], include("catalog.urlsCatalog")),
    url(r"^%s/"% catalog_url['ca'], include("catalog.urlsCatalog")),

    # catalog manage
    url(r'^catalogmanage/', include('catalog.urlsCatalogManage')),

    # manufacturer 
    url(r"^%s/" % manufacturer_url['en'], include("catalog.urlsManufacturer")),
    url(r"^%s/" % manufacturer_url['es'], include("catalog.urlsManufacturer")),
    url(r"^%s/" % manufacturer_url['ca'], include("catalog.urlsManufacturer")),

    # product 
    url(r"^%s/" % product_url['en'], include("catalog.urlsProduct")),
    url(r"^%s/" % product_url['es'], include("catalog.urlsProduct")),
    url(r"^%s/" % product_url['ca'], include("catalog.urlsProduct")),

    # contact
    url(r"^%s/" % contact_url['en'], include("contact.urlsContact")),
    url(r"^%s/" % contact_url['es'], include("contact.urlsContact")),
    url(r"^%s/" % contact_url['ca'], include("contact.urlsContact")),

    url(r'^search/', include('haystack.urls')),
    url(r"^partner/", include("partner.urlsPartner")),
    url(r"^sale/", include("sale.urlsSale")),
    url(r"^account/", include("account.urlsAccount")),
    url(r"^payment/", include("payment.urlsPayment")),
    url(r"^base/", include("base.urlsBase")),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r"^static/(?P<path>.*)$", "django.views.static.serve", {"document_root": MEDIA_ROOT}),

    # Ajax Paths
    url(r'^filemanager/', include('tools.filemanager.connector.urls')),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^jsi18n$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # Admin 
    url(r'^manager/', include(admin.site.urls)),
    url(r'^filebrowser/', include('filebrowser.urls')),

    #  Blog
    url(r"^blog/", include("blog.urlsBlog")),

    # Cms
    url(r"^cms/", include("tools.cms.urlsCms")),

    # Content
    url(r"^content/", include("content.urlsContent")),
    url(r"^(?P<content>[^/]+)", include("content.urlsContent")),
)
