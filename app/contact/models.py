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
from django.utils.translation import get_language, ugettext_lazy as _
from django import forms

from transmeta import TransMeta
from transurl import contact_url

from settings import LIVE_URL, LOCALE_URI, MEDIA_ROOT

class Contact(models.Model):
    """Contact Model"""
    __metaclass__ = TransMeta

    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('slug'), max_length=128, unique=True, help_text=_("This is a unique identifier that allows your contacts to display its detail view, ex 'how-can-i-contribute'"))
    default = models.BooleanField(_('Default'), default=False)
    email = models.CharField(_('Email'), max_length=128, blank=True)
    show_email = models.BooleanField(_('Show Email'), default=False)
    street = models.TextField(_('Street'), null=True, blank=True)
    zip = models.CharField(_('Zip'), max_length=128, null=True, blank=True)
    city = models.CharField(_('City'), max_length=128, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=128, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=128, null=True, blank=True)
    mobile_phone = models.CharField(_('Mobile Phone'), max_length=128, null=True, blank=True)
    fax = models.CharField(_('Fax'), max_length=128, null=True, blank=True)
    utm = models.CharField(_('UTM'), max_length=128, null=True, blank=True)
    twitter = models.CharField(_('Twitter'), max_length=128, null=True, blank=True)
    misc = models.TextField(_('Miscellaneous'), null=True, blank=True)
    status = models.BooleanField(_('Status'), default=False)
    logo  = models.ImageField(upload_to='contact/', blank=True, help_text=_("Resize image. Check documentation about logo template"))

    """ Custom fields model """

    class Meta:
        db_table = 'contact_contacts'
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if LOCALE_URI:
            url = '/%s/%s/%s' % (get_language(), contact_url[get_language()], self.slug)
        else:
            url = '/%s/%s' % (contact_url[get_language()], self.slug)
        return url

class ContactForm(forms.Form):
    """Contact Form"""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact_text = forms.CharField(widget=forms.Textarea)
