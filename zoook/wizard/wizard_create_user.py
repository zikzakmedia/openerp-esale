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

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

class create_user_wizard(osv.osv_memory):
    _name = 'zoook.create.user.wizard'

    def _col_get(self, cr, uid, context=None):
        result = []
        cols = self.pool.get('res.partner.address').search(cr, uid, [('partner_id','=',context['partner_id'])])
        for col in self.pool.get('res.partner.address').browse(cr, uid, cols):
            if col.name:
                name = col.name
            else:
                name = "/"
            result.append( (col.id, name) )
        result.sort()
        return result

    _columns = {
        'partner_address_id': fields.selection(_col_get, 'Address', method=True, required=True, size=32),
        'email_create_user': fields.many2one('poweremail.templates', 'Email', required=True, help='Template Email Create User'),
        'username': fields.char('Username', size=64, readonly=True),
        'password': fields.char('Password', size=64, readonly=True),
        'email': fields.char('Email', size=255, readonly=True),
        'first_name': fields.char('First Name', size=255, readonly=True),
        'last_name': fields.char('Last Name', size=255, readonly=True),
        'result': fields.text('Result', readonly=True),
        'state':fields.selection([
            ('first','First'),
            ('done','Done'),
        ],'State'),
    }

    _defaults = {
        'state': lambda *a: 'first',
    }

    def set_first_last_name(self, name, scape=False):
        """Split name to first name and last name"""
        # split name: first_name + name
        name = name.split(' ')
        if len(name) > 1:
            first_name = name[0]
            del name[0]
            last_name = " ".join(name)
        else:
            first_name = name[0]
            last_name = name[0]

        if scape:
            first_name = unicodedata.normalize('NFKD', first_name).encode('ascii','ignore')
            last_name = unicodedata.normalize('NFKD', last_name).encode('ascii','ignore')

        return first_name, last_name

    def create_user(self, cr, uid, ids, context=None):
        result = ''
        res_values = {}

        form = self.browse(cr, uid, ids[0])

        partner_id = context and context.get('partner_id')
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
        partner_address = self.pool.get('res.partner.address').browse(cr, uid, form.partner_address_id)

        if partner.dj_username or partner.dj_email:
            result = _('This Django user exist.')

        if not partner_address.email:
            result = _('This address there are not email. Please add new email for this address')

        useremail = self.pool.get('res.partner').search(cr, uid, [('dj_email','=',partner_address.email)])
        if len(useremail):
            result = _('This email exist another user. Use another email/address')

        if not result:
            #First Name / Last Name
            if partner_address.name:
                first_name, last_name = self.set_first_last_name(partner_address.name, True)
            else:
                first_name, last_name = self.set_first_last_name(partner.name, True)

            #Username
            username = slugify(partner.name)
            #exist this username?
            usernames = self.pool.get('res.partner').search(cr, uid, [('dj_username','=',username)])
            if len(usernames) > 0:
                username = username+str(len(usernames)+1)
            #Email
            email = partner_address.email
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
                context['command'] = 'sync/user.py -u %s -p %s -o %s -e %s -f "%s" -l "%s"' % (username, password, partner_id, email, first_name, last_name)
                respy = self.pool.get('django.connect').ssh_command(cr, uid, sale.id, values, context)
                res.append(_('Sale Shop: %s Username: %s. %s') % (sale.name, username, respy))

            if len(res)>0:
                for r in res:
                    result += r
            
            res_values['username'] = username
            res_values['password'] = password
            res_values['first_name'] = first_name
            res_values['last_name'] = last_name
            res_values['email'] = email

            #write partner dj info
            self.pool.get('res.partner').write(cr, uid, [partner_id], {'dj_username': username, 'dj_email': email})

        res_values['state'] = 'done'
        res_values['result'] = result
        #write result values
        self.write(cr, uid, ids, res_values)
        
        self.pool.get('poweremail.templates').generate_mail(cr, uid, form.email_create_user.id, [form.id])

        return True

create_user_wizard()
