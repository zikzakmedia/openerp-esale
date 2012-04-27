#!/usr/bin/env python
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

import os
import sys
import logging
import time
import optparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.utils.translation import ugettext as _
from catalog.models import ProductProduct, ProductTemplate, ProductCategory, ResManufacturer
from tools.conn import conn_webservice

logging.basicConfig(filename=LOGFILE,level=logging.INFO)
logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Running')))

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-p", "--products", dest="products",
                default=False,
                help="Get product list.")
options, args = parser.parse_args()

"""
for product.template
    for product.product
        if product.attributes
"""

"""Get Products to import at Django"""
prods = []
if options.products:
    prods = options.products.split(',')
results = conn_webservice('sale.shop', 'dj_export_products', [[OERP_SALE], prods])
logging.info('[%s] Total: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'),len(results)))

langs = conn_webservice('sale.shop', 'zoook_sale_shop_langs', [[OERP_SALE]])
langs = langs[str(OERP_SALE)]
context = {}

if len(results) == 0:
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Not products template news or modified')))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.template',[result['product_template']],context,langs])

    if DEBUG:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))

    if len(values) > 0:
        product_template = values[0]

        #detect m2m fiels (is a list) and add values
        prod_template = {}
        m2m_template = {}
        for k,v in product_template.iteritems():
            if type(v).__name__=='list':
                m2m_template[k] = v
            else:
                prod_template[k] = v
        
        # add manufacturer if available
        if 'manufacturer' in prod_template:
            manufacturer = prod_template['manufacturer']
            del prod_template['manufacturer']
            res_manufacturer = ResManufacturer.objects.filter(id=manufacturer)
            if res_manufacturer:
                prod_template['manufacturer'] = res_manufacturer[0]

        prod_template = ProductTemplate(**prod_template)

        # m2m fields
        #ptemplate = ProductTemplate(id=1,name_es='OpenERP Service')
        ##ptemplate.categ.clear()
        #ptemplate.categ.remove(8)
        #ptemplate.categ.add(3,6)
        #ptemplate.save()

        try:
            prod_template.save()
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Product Template save ID %s') % product_template['id']))
            logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.template', int(product_template['id']), 'done', 'Successfully save template'])
        except:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Error save ID %s') % product_template['id']))
            logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.template', int(product_template['id']), 'error', 'Error save template'])

        for k,v in m2m_template.iteritems():
            x = []
            for cat_id in v:
                #check if this product.category exists
                cat = ProductCategory.objects.filter(id=cat_id)
                if cat:
                    x.append(cat_id)
                else:
                    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. m2m NOT exist ID %s') % cat_id))

            try:
                getattr(prod_template, k).clear()
                getattr(prod_template, k).add(*x) #TODO: m2m fields deleted (not create all fields)
                prod_template.save()
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Save m2m ID %s') % product_template['id']))
                #~ prod_template.save_m2m()
            except:
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Template. Error save m2m %s - %s') % (k, v)))

        for prod in result['product_product']:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products Product. Get ID %s') % prod))

            # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
            context = {'shop':OERP_SALE, 'product_id': prod}
            values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.product',[prod],context,langs])

            if DEBUG:
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))

            if len(values) > 0:
                product = values[0]
                prod = ProductProduct(**product)
                try:
                    prod.save()
                    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Product save ID %s') % product['id']))
                    logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.product', int(product_template['id']), 'done', 'Successfully save product'])
                except:
                    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Error save ID %s') % product['id']))
                    logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.product', int(product_template['id']), 'error', 'Error save product'])

logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Products. Done')))

print True
