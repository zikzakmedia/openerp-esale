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

from django.conf.urls.defaults import *
from catalog.views import *

"""Urls Catalog Manage"""
urlpatterns = patterns("",
    #product home
    url(r"^producthome/edit/(?P<home_id>[^/]+)", 'catalog.views.product_home_edit', name='catalog_product_home_edit'),
    url(r"^producthome/add/", 'catalog.views.product_home_add', name='catalog_product_home_add'),
    url(r"^producthome/", 'catalog.views.product_home', name='catalog_product_home'),
    
    #product recommended
    url(r"^productrecommended/edit/(?P<recommended_id>[^/]+)", 'catalog.views.product_recommended_edit', name='catalog_product_recommended_edit'),
    url(r"^productrecommended/add/", 'catalog.views.product_recommended_add', name='catalog_product_recommended_add'),
    url(r"^productrecommended/", 'catalog.views.product_recommended', name='catalog_product_recommended'),
    
    #product offer
    url(r"^productoffer/edit/(?P<offer_id>[^/]+)", 'catalog.views.product_offer_edit', name='catalog_product_offer_edit'),
    url(r"^productoffer/add/", 'catalog.views.product_offer_add', name='catalog_product_offer_add'),
    url(r"^productoffer/", 'catalog.views.product_offer', name='catalog_product_offer'),
)
