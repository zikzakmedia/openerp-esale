# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Raimon Esteve <resteve@zikzakmedia.com>
#                       Jesus Martín <jmartin@zikzakmedia.com>
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
    
    def zoook_export_manufacturers(self, cr, uid, ids, context=None):
        """
        Sync Manufacturers. Sale Shop
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
            context['command'] = 'sync/manufacturer.py'

            thread1 = threading.Thread(target=self.zoook_export_manufacturers_thread, args=(cr.dbname, uid, sale.id, values, context))
            thread1.start()
            
        return True

    def zoook_export_manufacturers_thread(self, db_name, uid, sale, values, context=None):
        """Thread Export Images
        :sale: Sale Shop ID (int)
        :values: Dicc
        :context: Dicc
        return True/False
        """
        db, pool = pooler.get_db_and_pool(db_name)
        cr = db.cursor()

        manufacturer = self.pool.get('django.connect').ssh_command(cr, uid, sale, values, context)

        cr.commit()
        cr.close()

        if manufacturer:
            LOGGER.notifyChannel('ZoooK Connection', netsvc.LOG_INFO, "Manufacturers Export Running.")
            return True
        else:
            LOGGER.notifyChannel('ZoooK Connection', netsvc.LOG_ERROR, "Error connection to server.")
            return False

sale_shop()
