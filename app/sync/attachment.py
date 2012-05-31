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
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.utils.translation import ugettext as _
from base.models import IrAttachment
from tools.conn import conn_webservice
from tools.zoook import connOOOP, call_command

logging.basicConfig(filename=LOGFILE,level=logging.INFO)
logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Attachment. Running')))

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage)
parser.add_option("-r", "--resource", dest="resources",
                default=False,
                help="Get product list.")
options, args = parser.parse_args()

"""Get Attachment to import at Django"""
resources = []
if options.resources:
    resources = options.resources.split(',')

conn = connOOOP()
if not conn:
    logging.info('[%s] %s' % ('Error connecting to ERP'))

results = conn_webservice('sale.shop', 'dj_export_attachments', [[OERP_SALE], resources])
logging.info('[%s] Total: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'),len(results)))

if len(results) == 0:
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Not resources news or modified')))

for res in results:
    result = conn.IrAttachment.get(res)

    values = {
        'id': result.id,
        'name': result.name,
        'description': result.description and result.description or '',
        'res_name': result.res_name,
        'res_model': result.res_model,
        'res_id': result.res_id,
        'datas_fname': result.datas_fname,
        'type': result.type,
        'store_fname': result.store_fname,
        'store_fslug': re.sub('/', '-', result.store_fname),
        'file_size': result.file_size,
        'file_type': result.file_type,
        'visibility': result.esale_visibility,
    }
    attachment = IrAttachment(**values)
    try:
        attachment.save()
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Attachment save ID %s') % result.id))
    except:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), _('Sync. Attachment. Error save ID %s') % result.id))

#rsync openerp server to local
if ATTACHMENT_SYNC:
    error = False
    command = 'rsync -e "ssh -p %s %s" -az %s %s:%s %s' % (
            ATTACHMENT_SERVER_PORT,
            ATTACHMENT_SSH_OPTION,
            ATTACHMENT_RSYNC_OPTION,
            ATTACHMENT_SERVER,
            ATTACHMENT_SOURCE,
            ATTACHMENT_ROOT,
    )
    logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Start command: %s' % command))

    output,_,result = call_command(command)
    error = error or result

    if error:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'RSync. Error: %s' % error))
    else:
        logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'RSync. Done %s' % ATTACHMENT_SERVER))

logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), 'Sync. Attachment. Done'))

print True
