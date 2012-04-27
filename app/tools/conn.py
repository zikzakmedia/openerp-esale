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

from django.utils.translation import get_language

from settings import *

from ooop import OOOP
import xmlrpclib

# check if pyro is installed
try:
    import Pyro.core
except:
    pyro = False

from settings import OERP_CONF

def conn_ooop():
    """Connection OpenERP throught OOOP"""
    
    lang = LOCALES.get(get_language(),'en_US')
    try:
        #o = OOOP(user='admin',pwd='admin',dbname='oerp6_zoook',uri='http://localhost',port=8069,protocol='xmlrpc')
        #o = OOOP(user='admin',pwd='admin',dbname='oerp6_zoook',uri='localhost',port=8071,protocol='pyro')
        conn = OOOP(
                user=OERP_CONF['username'],
                pwd=OERP_CONF['password'],
                dbname=OERP_CONF['dbname'],
                uri=OERP_CONF['uri'],
                port=OERP_CONF['port'],
                protocol=OERP_CONF['protocol'],
                lang=lang,
                debug=DEBUG,
            )
        return conn
    except:
        return False

def xmlrpc():
    """Connection OpenERP with XMLRPC"""
    try:
        # Get the uid
        server_common = '%s:%s/xmlrpc/common' % (OERP_CONF['uri'],OERP_CONF['port'])
        server_object = '%s:%s/xmlrpc/object' % (OERP_CONF['uri'],OERP_CONF['port'])

        sock_common = xmlrpclib.ServerProxy(server_common)
        uid = sock_common.login(OERP_CONF['dbname'], OERP_CONF['username'], OERP_CONF['password'])
        server_object = '%s:%s/xmlrpc/object' % (OERP_CONF['uri'],OERP_CONF['port'])
        sock = xmlrpclib.ServerProxy(server_object)
        return uid, sock
    except:
        return False

def pyro():
    """Connection OpenERP with PYRO"""
    try:
        # Get the uid
        url = 'PYROLOC://%s:%s/rpc' % (OERP_CONF['uri'],OERP_CONF['port'])

        proxy = Pyro.core.getProxyForURI(url)
        uid = proxy.dispatch( 'common', 'login', OERP_CONF['dbname'], OERP_CONF['username'], OERP_CONF['password'])
        return uid, proxy
    except:
        return False

def conn_webservice(model, call, values=[]):
    """Connection OpenERP with webservice
    model: OpenERP model
    call: def model
    values: list parameters

    Example call:
    results = conn_webservice(model, call, values)
    """

    if OERP_CONF['protocol'] == 'pyro':
        uid, proxy = pyro()
        results = proxy.dispatch( 'object', 'execute', OERP_CONF['dbname'], uid, OERP_CONF['password'], model, call, *values)
    else:
        uid, sock = xmlrpc()
        results = sock.execute(OERP_CONF['dbname'], uid, OERP_CONF['password'], model, call, *values)

    return results
