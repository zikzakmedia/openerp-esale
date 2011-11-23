# -*- encoding: utf-8 -*-
############################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
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
############################################################################################

from osv import fields,osv
from tools.translate import _

import re
import unicodedata
import random
import string

class reset_user_wizard(osv.osv_memory):
    _name = 'zoook.reset.user.wizard'

    _columns = {
        'email_reset_user': fields.many2one('poweremail.templates', 'Email', required=True, help='Template Email Reset User'),
        'partner_id': fields.many2one('res.partner', 'Partner'),
        'username': fields.char('Username', size=64, readonly=True),
        'password': fields.char('Password', size=64, readonly=True),
        'result': fields.text('Result', readonly=True),
        'state':fields.selection([
            ('first','First'),
            ('done','Done'),
        ],'State'),
    }

    _defaults = {
        'partner_id': lambda s,cr,uid,context: context['partner_id'],
        'state': lambda *a: 'first',
    }

    def reset_user(self, cr, uid, ids, context=None):
        result = ''
        res_values = {}

        form = self.browse(cr, uid, ids[0])

        partner_id = context and context.get('partner_id')
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id)

        if partner.dj_username or partner.dj_email:
            #Password
            char_set = string.ascii_uppercase + string.digits
            password = ''.join(random.sample(char_set,6))

            res = []
            sale_shop_ids = self.pool.get('sale.shop').search(cr, uid, [('zoook_shop','=',True)])
            if len(sale_shop_ids) == 0:
                result = _('Error: Sale Shop not active')

            for sale in self.pool.get('sale.shop').browse(cr, uid, sale_shop_ids):
                values = {
                    'ip': sale.zoook_ip,
                    'port': sale.zoook_port,
                    'username': sale.zoook_username,
                    'password': sale.zoook_password,
                    'key': sale.zoook_key,
                    'ssh_key': sale.zoook_ssh_key,
                    'basepath': sale.zoook_basepath,
                }
                context['command'] = 'sync/user_reset.py -u %s -p %s' % (partner.dj_username, password)
                respy = self.pool.get('django.connect').ssh_command(cr, uid, sale.id, values, context)
                res.append(_('Sale Shop: %s Username: %s. %s') % (sale.name, partner.dj_username, respy))

            if len(res)>0:
                for r in res:
                    result += r
            
            res_values['username'] = partner.dj_username
            res_values['password'] = password

        res_values['state'] = 'done'
        res_values['result'] = result
        #write result values
        self.write(cr, uid, ids, res_values)
        
        self.pool.get('poweremail.templates').generate_mail(cr, uid, form.email_reset_user.id, [form.id])

        return True

reset_user_wizard()
