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
from tools.translate import _

import netsvc
import time
import datetime

class esale_log(osv.osv):
    _name = 'esale.log'
    _description = 'eSale Logs'
    _order = "id desc"

    _columns = {
        'create_log': fields.datetime('Create'),
        'sale_shop_id': fields.many2one('sale.shop', 'Sale Shop', required=True),
        'model_id': fields.many2one('ir.model', 'OpenERP Model', required=True, select=True, ondelete='cascade'),
        'oerp_id': fields.integer('OpenERP ID', required=True),
        'mgn_id': fields.integer('Magento ID'),
        'status': fields.selection([
            ('done', 'Done'),
            ('error', 'Error'),
        ], 'Status'),
        'comment': fields.char('Comment', size=256),
    }

    def create_log(self, cr, uid, shop, model, oerp_id, status = 'done', comment = ''):
        """
        Create new log
        :param shop: Sale Shop ID
        :param model: str name model
        :param oerp_id: int OpenERP ID
        :return magento_external_referential_id
        """
        model_ids = self.pool.get('ir.model').search(cr, uid, [('model','=',model)])

        values = {
            'create_log': time.strftime('%Y-%m-%d %H:%M:%S'),
            'sale_shop_id': shop,
            'model_id': model_ids[0],
            'oerp_id': oerp_id,
            'status': status,
            'comment': comment,
        }
        esale_log_id = self.create(cr, uid, values)
        cr.commit()

        return esale_log_id

    def run_clean_log_scheduler(self, cr, uid, use_new_cursor=False, context=None):
        """eSale - Clean Logs
        Delete logs from date to past
        """

        esale_log_obj = self.pool.get('esale.log')
        sale_shop_obj = self.pool.get('sale.shop')

        sale_shops = sale_shop_obj.search(cr, uid, [('zoook_shop','=',True)])
        for sale_shop in sale_shop_obj.browse(cr, uid, sale_shops):
            day = int(sale_shop.zoook_log_clean)
            if day:
                date = datetime.date.today()-datetime.timedelta(days=day)
                from_date = "%s 00:00:00" % (date)
                logs = esale_log_obj.search(cr, uid, [('create_log', '<', from_date),('sale_shop_id','=',sale_shop.id)])
                esale_log_obj.unlink(cr, uid, logs)

        return True

esale_log()
