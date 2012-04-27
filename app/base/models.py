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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from transmeta import TransMeta

'''OpenERP Models'''
class ResCountry(models.Model):
    """Country OpenERP"""
    __metaclass__ = TransMeta

    code = models.CharField(_('code'), max_length=2)
    name = models.CharField(_('name'), max_length=64)
    status = models.BooleanField(_('status'), default=True)

    class Meta:
        db_table = 'res_country'
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        translate = (
            'name',
            )

    def __unicode__(self):
        return self.name

class ResCountryState(models.Model):
    """Country State OpenERP"""

    code = models.CharField(_('State Code'), max_length=128, null=True, blank=True)
    country = models.ForeignKey('ResCountry', null=True, blank=True)
    name = models.CharField(_('State Name'), max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'res_country_state'
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __unicode__(self):
        return self.name
