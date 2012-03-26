# -*- encoding: utf-8 -*-
############################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from osv import fields,osv
from tools.translate import _

import pooler
import threading

class zoook_sync_product_wizard(osv.osv_memory):
    _name = 'zoook.sync.product.wizard'

    def _zoook_sale_shop(self, cr, uid, context=None):
        ids = self.pool.get('sale.shop').search(cr, uid, [('zoook_shop', '=', True)], order='id')
        shops = self.pool.get('sale.shop').read(cr, uid, ids, ['id','name'], context=context)
        return [(a['id'], a['name']) for a in shops]

    _columns = {
        'zoook_sale_shop': fields.selection(_zoook_sale_shop, 'Sale Shop', required=True),
        'result': fields.text('Result', readonly=True),
        'state':fields.selection([
            ('first','First'),
            ('done','Done'),
        ],'State'),
    }

    _defaults = {
        'state': lambda *a: 'first',
    }

    def sync_product(self, cr, uid, ids, data, context={}):
        """Export sync products"""

        if len(data['active_ids']) == 0:
            raise osv.except_osv(_('Error!'), _('Select products to export'))

        form = self.browse(cr, uid, ids[0])
        shop = form.zoook_sale_shop
        shop = self.pool.get('sale.shop').browse(cr, uid, shop)

        product_ids = []
        for prod in self.pool.get('product.product').browse(cr, uid, data['active_ids']):
            if prod.product_tmpl_id.zoook_exportable:
                product_ids.append(prod.product_tmpl_id.id)

        values = {
            'state':'done',
        }
        if len(product_ids) > 0:
            values['result'] = '%s' % (', '.join(str(x) for x in product_ids))
        else:
            values['result'] = _('Not available some e-Sale Products to export')

        self.write(cr, uid, ids, values)

        cr.commit()

        if len(product_ids) > 0:
            values = {
                'ip': shop.zoook_ip,
                'port': shop.zoook_port,
                'username': shop.zoook_username,
                'password': shop.zoook_password,
                'key': shop.zoook_key,
                'ssh_key': shop.zoook_ssh_key,
                'basepath': shop.zoook_basepath,
            }

            context['command'] = 'sync/product.py -p %s' % (','.join(str(x) for x in product_ids))
            thread1 = threading.Thread(target=self.pool.get('sale.shop').zoook_export_products_thread, args=(cr.dbname, uid, shop.id, values, context))
            thread1.start()
        return True

zoook_sync_product_wizard()


