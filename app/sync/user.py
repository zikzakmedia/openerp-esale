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
from partner.models import *

logging.basicConfig(filename=LOGFILE,level=logging.INFO)

if __name__=="__main__":
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-u", "--username", dest="username", type="string", help="User Name")
    parser.add_option("-p", "--password", dest="password", type="string", help="Password")
    parser.add_option("-o", "--uid", dest="uid", type="int", help="OpenERP Partner ID")
    parser.add_option("-e", "--email", dest="email", type="string", help="Email")
    parser.add_option("-f", "--first_name", dest="fname", type="string", help="First Name")
    parser.add_option("-l", "--last_name", dest="lname", type="string", help="Last Name")

    (options, args) = parser.parse_args()

    error = []
    if not options.username:
        error.append(_('User. Username not available'))
        
    if not options.password:
        error.append(_('User. Password not available - %s') % options.username)

    if not options.uid:
        error.append(_('User. User ID not available - %s') % options.username)
        
    if not options.email:
        error.append(_('User. Email not available - %s') % options.username)
        
    if not options.fname:
        error.append(_('User. First Name not available - %s') % options.username)
        
    if not options.lname:
        error.append(_('User. Last Name not available - %s') % options.username)

    if len(error) > 0:
        for err in error:
            logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), err))
            print err
    else:
        users = User.objects.filter(username__exact=options.username)
        emails = User.objects.filter(email__exact=options.email)

        if users:
            error.append(_('User. This user exist - %s') % options.username)
        if emails:
            error.append(_('User. This email exist - %s') % options.email)

        if len(error) > 0:
            for err in error:
                logging.info('[%s] %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), err))
                print err
        else:
            user = User.objects.create_user(options.username, options.email, options.password)
            user.first_name = options.fname
            user.last_name = options.lname
            user.is_staff = False
            user.save()

            # create authProfile
            authProfile = AuthProfile(user=user,partner_id=options.uid)
            authProfile.save()
            
            print True

