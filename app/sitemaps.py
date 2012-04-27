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

from django.contrib.sitemaps import Sitemap

from content.models import Content
from catalog.models import ProductCategory, ProductTemplate

""" Content Sitemap """
class ContentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Content.objects.filter(status=True)

""" Catalog Sitemap """
class ProductCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ProductCategory.objects.filter(status=True)

class ProductProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ProductTemplate.objects.filter(status=True)

sitemaps = {
    'content':ContentSitemap(),
    'productproduct':ProductProductSitemap(),
    'productcategory':ProductCategorySitemap(),
}
