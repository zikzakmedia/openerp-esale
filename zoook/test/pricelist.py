# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
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

import xmlrpclib

username = 'admin'  #the user
pwd = 'admin'       #the password of the user
dbname = 'oerp6_zoook'    #the database

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

shop_id = 1
#id product : quantity
products = [
    {
        'product_id':1,
        'quantity':15,
    },
    {
        'product_id':2,
        'quantity':342,
    },
    {
        'product_id':3,
        'quantity':452,
    },
    {
        'product_id':4,
        'quantity':542,
    },
]

partner_id = 4

product_price = sock.execute(dbname, uid, pwd, 'product.product', 'zoook_compute_price', shop_id, products, partner_id)

#return  => {"1":{"regularPrice":"50"},"2":{"regularPrice":"100"}}
print "Product price = %s" % product_price
for prod in product_price:
    print "Product Price %s: %s" % (prod, product_price[prod])
    

