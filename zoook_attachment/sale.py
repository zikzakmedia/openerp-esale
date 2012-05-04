# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Raimon Esteve <resteve@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from datetime import datetime
from tools.translate import _

import netsvc
import time
import tools
import pooler
import threading

LOGGER = netsvc.Logger()

class sale_shop(osv.osv):
    _inherit = "sale.shop"
    
    _columns = {
        'esale_last_export_attachment': fields.datetime('Last Export Attachment'),
    }

    def esale_export_attachment(self, cr, uid, ids, context=None):
        """ 
        Sync Attachment. Sale Shop
        Execute external command (sync)
        """

        res = {}

        for sale in self.browse(cr, uid, ids):
            values = {
                'ip': sale.zoook_ip,
                'port': sale.zoook_port,
                'username': sale.zoook_username,
                'password': sale.zoook_password,
                'key': sale.zoook_key,
                'ssh_key': sale.zoook_ssh_key,
                'basepath': sale.zoook_basepath,
            }
            context['command'] = 'sync/attachment.py'

            thread1 = threading.Thread(target=self.esale_export_attachment_thread, args=(cr.dbname, uid, sale.id, values, context))
            thread1.start()

        return True

    def esale_export_attachment_thread(self, db_name, uid, sale, values, context=None):
        """Thread Export Products
        :sale: Sale Shop ID (int)
        :values: Dicc
        :context: Dicc
        return True/False
        """
        db, pool = pooler.get_db_and_pool(db_name)
        cr = db.cursor()

        product = self.pool.get('django.connect').ssh_command(cr, uid, sale, values, context)

        cr.commit()
        cr.close()

        if product:
            LOGGER.notifyChannel('e-Sale', netsvc.LOG_INFO, "Attachment Export Running.")
            return True
        else:
            LOGGER.notifyChannel('e-Sale', netsvc.LOG_ERROR, "Error connection to server.")
            return False

    def dj_export_attachments(self, cr, uid, ids, resources=[], context=None):
        """
        @param ids: Sale Shop IDs
        @param resources: Resource IDS
        Return list with attachment IDs
        """

        attachment_obj = self.pool.get('ir.attachment')

        res = []
        if len(resources)>0: #sync attachment by wizard
            for resource in resources:
                resource_id = int(resource)
                res.append(resource_id)
        else: #sync attachment by cron
            for shop in self.browse(cr, uid, ids):
                last_exported_time = shop.esale_last_export_attachment
                attchs = attachment_obj.search(cr, uid, [('esale_exportable','=',True),('esale_saleshop_ids','in',shop.id)])

                for att in attachment_obj.perm_read(cr, uid, attchs):
                    attach = False
                    # attachment create/modify > date exported last time
                    if last_exported_time < att['create_date'][:19] or (att['write_date'] and last_exported_time < att['write_date'][:19]):
                        attach = True

                    if attach:
                        res.append(att['id'])
 
            self.write(cr, uid, [shop.id], {'esale_last_export_attachment': time.strftime('%Y-%m-%d %H:%M:%S')})

            LOGGER.notifyChannel('e-Sale', netsvc.LOG_INFO, "Attachment: %s" % (res) )

        return res

sale_shop()
