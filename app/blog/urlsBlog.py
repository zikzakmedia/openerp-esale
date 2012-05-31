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
from blog.views import *
from blog.feeds import *

"""Urls Blog"""

urlpatterns = patterns("",
    url(r'^$', 'blog.views.blog_list', name='blog_list'),
    url(r"^edit/(?P<blog_id>[^/]+)", 'blog.views.blog_edit', name='blog_edit'),
    url(r"^add/", 'blog.views.blog_add', name='blog_add'),
    url(r"^key/(?P<key>[^/]+)/", 'blog.views.blog_list', name='blog_key'),
    url(r"^rss/$", BlogFeed()),
    url(r"^(?P<blog>[^/]+)", 'blog.views.blog_detail', name='blog_blog'),
)
