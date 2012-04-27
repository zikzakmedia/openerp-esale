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

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from django.utils.translation import ugettext as _

from django.contrib.sites.models import Site 
from tools.cms.models import SiteConfiguration

site = Site.objects.get(id=SITE_ID)
if site:
    values = {
        'site_ptr': site,
        'domain': site.domain,
        'name': site.name,
    }
    exclude_fields = ['id','domain','name','site_ptr']
    
    print "Add new configuration %s" % site.domain
    
    for field in SiteConfiguration._meta.fields:
        if field.name not in exclude_fields:
            values[field.name] = raw_input('%s: ' % field.name)

    site_configuration = SiteConfiguration(**values)

    try:
        site_configuration.save()
        print "Add new site configuration: %s" % site_configuration.domain
        print "Start your Django APP: python manage runserver"
        print "Remember to clone Products and Categories OpenERP -> Django"
    except:
        print "Ups! Not save values? Try insert sql command..."
        print values
else:
    print "SITE ID Object not found"
