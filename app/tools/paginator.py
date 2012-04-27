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

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from settings import PAGINATION_DEFAULT_TOTAL

def set_paginator_options(request, default = 'position'):
    """Paginator options
    :return None"""

    if 'paginator' in request.session:
        request.session['paginator'] = request.GET.get('paginator') and int(request.GET.get('paginator')) or request.session['paginator'] or PAGINATION_DEFAULT_TOTAL
    else:
        request.session['paginator'] = request.GET.get('paginator') and int(request.GET.get('paginator')) or PAGINATION_DEFAULT_TOTAL

    # mode options = session
    if 'mode' in request.session:
        request.session['mode'] = request.GET.get('mode') and request.GET.get('mode') or request.session['mode'] or 'grid'
    else:
        request.session['mode'] = request.GET.get('mode') and request.GET.get('mode') or 'grid'

    # order options = session
    if 'order' in request.session:
        request.session['order'] = request.GET.get('order') and request.GET.get('order') or request.session['order'] or default
    else:
        request.session['order'] = request.GET.get('order') and request.GET.get('order') or default

    # order_by options = session
    if 'order_by' in request.session:
        request.session['order_by'] = request.GET.get('order_by') and request.GET.get('order_by') or request.session['order_by'] or 'asc'
    else:
        request.session['order_by'] = request.GET.get('order_by') and request.GET.get('order_by') or 'asc'

def get_num_pages(objects, num_page_items):
    """Get Num Pages
    :obects: list or class
    :num_page_items: int
    :return int
    """
    if isinstance(objects, list):
        total = len(objects)
    else:
        total = objects.count()
    num_pages = total / num_page_items
    if num_pages == 0:
        return 1
    if total % num_page_items: num_pages += 1
    return num_pages
