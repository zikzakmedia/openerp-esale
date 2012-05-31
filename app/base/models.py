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

class IrAttachment(models.Model):
    """Ir Attachment OpenERP"""

    name = models.CharField(_('Name'), max_length=256)
    description = models.TextField(_('Description'), null=True, blank=True)
    res_name = models.CharField(_('Resource Object'), max_length=128)
    res_model = models.CharField(_('Name'), max_length=256)
    res_id = models.IntegerField(_('Resource ID'))
    datas_fname = models.CharField(_('File Name'), max_length=256)
    TYPE_CHOICES = (
        ('binary', 'Binary'),
        ('url', 'Url'),
    )
    type = models.CharField(_('type'), choices=TYPE_CHOICES, default='', max_length=40)
    store_fname = models.CharField(_('Store File Name'), max_length=256)
    store_fslug = models.CharField(_('Store File Slug'), max_length=256) # directory and file name by -
    file_size = models.IntegerField(_('File Size'))
    file_type = models.CharField(_('File Type'), max_length=128)
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('register', 'Register'),
        ('none', 'None'),
    )
    visibility = models.CharField(_('visibility'), choices=VISIBILITY_CHOICES, default='', max_length=40)

    class Meta:
        db_table = 'ir_attachment'
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __unicode__(self):
        return self.name

