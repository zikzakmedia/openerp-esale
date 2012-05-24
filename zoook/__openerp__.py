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

{
    "name" : "ZoooK - OpenERP e-sale",
    "version" : "1.0",
    "author" : "Zikzakmedia SL",
    "website" : "www.zikzakmedia.com",
    "category" : "Generic Modules",
    "description": """
    e-commerce management 100% integration by OpenERP.
    www.zikzakmedia.com/es/openerp-tiendas-virtuales
    """,
    "license" : "AGPL-3",
    "depends" : [
        "account_payment_extension",
        "base",
        "base_vat",
        "currency_numeric_code",
        'delivery',
        "django",
        "poweremail",
        "product_special_price",
        "product_m2mcategories",
        "product_images_olbs",
        "sale_margin",
        "sale_payment",
        "sale_promotions",
    ],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        "security/ir.model.access.csv",
        "settings/django_mapping.xml",
        "wizard/wizard_create_user.xml",
        "wizard/wizard_product_product.xml",
        "wizard/wizard_product_image.xml",
        "wizard/wizard_reset_user.xml",
        "base_view.xml",
        "delivery_view.xml",
        "partner_view.xml",
        "product_view.xml",
        "product_images_view.xml",
        "sale_view.xml",
        "esale_view.xml",
        "settings/zoook_data.xml",
    ],
    "active": False,
    "installable": True
}
