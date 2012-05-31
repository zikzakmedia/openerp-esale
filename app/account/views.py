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

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from settings import *
from tools.conn import conn_webservice
from tools.zoook import checkPartnerID, checkFullName, connOOOP, paginationOOOP

_('draft')
_('proforma')
_('proforma2')
_('open')
_('paid')
_('cancel')

"""Invoices. All Invoices Partner Available"""
@login_required
def invoices(request):
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    
    values = {}
    total = len(conn.AccountInvoice.filter(partner_id=partner_id, state__ne='draft', type='out_invoice', company_id=OERP_COMPANY))
    offset, page_previous, page_next = paginationOOOP(request, total, PAGINATOR_INVOICE_TOTAL)

    values = conn.AccountInvoice.filter(partner_id=partner_id, state__ne='draft', type='out_invoice', company_id=OERP_COMPANY, offset=offset, limit=PAGINATOR_INVOICE_TOTAL, order='name DESC')

    title = _('All Invoices')
    metadescription = _('List all invoices of %s') % full_name

    return render_to_response("account/invoices.html", {'title':title, 'metadescription':metadescription, 'values':values, 'page_previous':page_previous, 'page_next':page_next}, context_instance=RequestContext(request))

"""Invoice. Invoice Detail Partner"""
@login_required
def invoice(request, invoice):
    partner_id = checkPartnerID(request)
    if not partner_id:
        error = _('Are you a customer? Please, contact us. We will create a new role')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))
    full_name = checkFullName(request)
    conn = connOOOP()
    if not conn:
        error = _('Error when connecting with our ERP. Try again or cantact us')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    values = conn.AccountInvoice.filter(partner_id=partner_id, number=invoice, state__ne='draft', type='out_invoice', company_id=OERP_COMPANY)
    if len(values) == 0:
        error = _('It is not allowed to view this section or not found. Use navigation menu.')
        return render_to_response("partner/error.html", locals(), context_instance=RequestContext(request))

    value = values[0]
    title = _('Invoice %s') % (value.number)
    metadescription = _('Details invoice %s') % (value.number)

    return render_to_response("account/invoice.html", {'title': title, 'metadescription': metadescription, 'value': value}, context_instance=RequestContext(request))
