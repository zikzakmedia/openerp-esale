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
from partner.views import *
from tools.cms.views import *

"""Urls Cms"""
urlpatterns = patterns("",
    url(r"^modules/edit/(?P<modules_id>[^/]+)", 'tools.cms.views.modules_edit', name='cms_modules_edit'),
    url(r"^modules/add/", 'tools.cms.views.modules_add', name='cms_modules_add'),
    url(r"^modules/list/", 'tools.cms.views.modules_list', name='cms_modules'),
)
