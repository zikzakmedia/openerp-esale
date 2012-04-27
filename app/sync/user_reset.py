#!/usr/bin/env python
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

import os
import sys
import logging
import time
import optparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

logging.basicConfig(filename=LOGFILE,level=logging.INFO)

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-u", "--username", dest="username", type="string", help="User Name")
    parser.add_option("-p", "--password", dest="password", type="string", help="Password")

    (options, args) = parser.parse_args()

    error = []
    if not options.username:
        error.append(_('User. Username not available'))
        
    if not options.password:
        error.append(_('User. Password not available - %s') % options.username)

    if len(error) > 0:
        for err in error:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), err))
            print err
    else:
        users = User.objects.filter(username__exact=options.username)

        if not users:
            error.append(_('User. This user not exist - %s') % options.username)

        if len(error) > 0:
            for err in error:
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), err))
                print err
        else:
            user = users[0]
            user.set_password(options.password)
            user.save()

            print True

