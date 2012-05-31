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

from django.contrib.syndication.views import Feed
from django.utils.translation import get_language

from tools.zoook import siteConfiguration
from blog.models import Blog
from settings import *

class BlogFeed(Feed):
    site_configuration = siteConfiguration(SITE_ID)

    title = site_configuration.site_title
    if LOCALE_URI:
        link = "/%s/blog/" % get_language()
    else:
        link = ''
    description = site_configuration.site_metadescription

    def items(self):
        site_configuration = siteConfiguration(SITE_ID)
        return Blog.objects.order_by('-created_on')[:site_configuration.rss_max]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description
