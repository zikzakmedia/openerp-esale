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
from catalog.models import ProductImages
from tools.conn import conn_webservice

logging.basicConfig(filename=LOGFILE,level=logging.INFO)
logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Images. Running')))

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-p", "--products", dest="products",
                default=False,
                help="Get product list.")
options, args = parser.parse_args()

products = []
if options.products:
    products = options.products.split(',')

results = conn_webservice('sale.shop', 'dj_export_images', [[OERP_SALE], products])

if len(results) == 0:
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Images. Not images news or modified')))

for result in results:
    # minicalls with one id (step to step) because it's possible return a big dicctionay and broken memory.
    context = {'shop':OERP_SALE}
    values = conn_webservice('base.external.mapping', 'get_oerp_to_external', ['zoook.product.images',[result],context])

    if DEBUG:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), values))

    if len(values) > 0:
        img = values[0]
        image = ProductImages(**img)
        try:
            image.save()
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Images. Image save ID %s') % img['id']))
            logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.images', int(img['id']), 'done', 'Successfully save image'])
        except:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Images. Error save ID %s') % img['id']))
            logs = conn_webservice('esale.log', 'create_log', [OERP_SALE, 'product.images', int(img['id']), 'error', 'Error save image'])

logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Images. Done')))

print True
