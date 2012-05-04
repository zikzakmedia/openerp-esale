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

class ir_attachment(osv.osv):
    _inherit = "ir.attachment"

    _columns = {
        'esale_exportable':fields.boolean('Available e-sale', change_default=True,),
        'esale_visibility': fields.selection([
                    ('public', 'Public'),
                    ('register', 'Register'),
                    ('none', 'None'),
                    ], 'Visibility'),
        'esale_saleshop_ids': fields.many2many('sale.shop', 'zoook_attachment_sale_shop_rel', 'attachment_id', 'sale_shop_id', 'Websites', help='Select yours Sale Shops available this attachment'),
    }

    _defaults = {
        'esale_visibility': lambda *a: 'public',
    }

    def unlink(self, cr, uid, ids, context=None):
        """Dissable unlink attachment available esale export"""

        for attach in self.read(cr, uid, ids, ['esale_exportable']):
            esale = attach.get('esale_exportable', False)
            if esale:
                raise osv.except_osv(_("Alert"), _("To Unlink this attachment mark visibility is none"))

        return super(ir_attachment, self).unlink(cr, uid, ids, context)

ir_attachment()
