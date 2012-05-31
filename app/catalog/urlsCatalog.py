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
from catalog.views import *
from catalog.feeds import *

"""Urls Catalog"""
urlpatterns = patterns("",
    url(r'^$', 'catalog.views.index', name='catalog_index'),
    url(r"^updateprice", 'catalog.views.updateprice', name='catalog_updateprice'),
    url(r"^compare", 'catalog.views.compare', name='catalog_compare'),
    url(r"^whistlist", 'catalog.views.whistlist', name='catalog_whistlist'),
    url(r"^rss/$", ProductFeed()),
    url(r"^.+/(?P<category>[^/]+)/$", 'catalog.views.category', name='catalog_category_child'),
    url(r"(?P<category>[^/]+)/$", 'catalog.views.category', name='catalog_category'),
)
