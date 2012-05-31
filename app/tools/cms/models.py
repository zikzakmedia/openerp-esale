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
from django.contrib.sites.models import Site 

from transmeta import TransMeta

import tools.cms.enums as enums

class SiteConfiguration(Site):
    """Site Configuration Management"""
    __metaclass__ = TransMeta

    site_title = models.CharField(_('site title'),max_length=150)
    site_slogan = models.CharField(_('site slogan'),max_length=150, blank=True)
    site_footer1 = models.TextField( _('footer 1'), blank=True)
    site_footer2 = models.TextField( _('footer 2'), blank=True)
    site_metadescription = models.CharField(_('site metadescription'),max_length=150)
    site_metakeywords = models.CharField(_('site metakeywords'),max_length=150)
    contact_email = models.TextField(_('contact emails'), help_text=_('Separated by comma (,)') )
    rss_max = models.FloatField(_('rss max'))

    class Meta:
        db_table = 'site_configuration'
        verbose_name = _('configuration')
        verbose_name_plural = _('configurations')
        translate = (
            'site_title',
            'site_slogan',
            'site_metadescription',
            'site_metakeywords',
        )

class Menu(models.Model):
    """Menu Management"""
    __metaclass__ = TransMeta
    
    name = models.CharField(_('name'),max_length=100)
    slug = models.SlugField(_('slug'),)
    base_url = models.CharField(_('base url'),max_length=100, blank=True, null=True)
    description = models.TextField(_('description'),blank=True, null=True)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __unicode__(self):
        return "%s" % self.name

    def save(self):
        """
        Re-order all items at from 10 upwards, at intervals of 10.
        This makes it easy to insert new items in the middle of 
        existing items without having to manually shuffle 
        them all around.
        """
        super(Menu, self).save()

        current = 10
        for item in MenuItem.objects.filter(menu=self).order_by('order'):
            item.order = current
            item.save()
            current += 10
 
class MenuItem(models.Model):
    """Menu Items"""
    __metaclass__ = TransMeta

    menu = models.ForeignKey(Menu)
    title = models.CharField(_('title'),max_length=100)
    link_url = models.CharField(_('link url'),max_length=100, help_text=_('URL or URI, eg /about/ or http://foo.com/'))
    order = models.IntegerField(_('order'),)
    css = models.CharField(_('css class'),max_length=100, blank=True)
    login_required = models.BooleanField(_('login required'),)
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_ACTIVE, help_text=_("Only items with their status set to 'Active' will be displayed."))

    class Meta:
        verbose_name = _('menus item')
        verbose_name_plural = _('menus items')
        translate = ('title', 'link_url')
        ordering = ['order']

    def __unicode__(self):
        return "%s %s. %s" % (self.menu.slug, self.order, self.title)

class Modules(models.Model):
    """
    Modules Management
    """
    __metaclass__ = TransMeta

    name = models.CharField(_('name'), max_length=255)
    position = models.CharField(_('position'), max_length=255, help_text=_("This is a unique identifier, ex 'position1'"))
    description = models.TextField(verbose_name=_('description'))
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_ACTIVE, help_text=_("Only modules with their status set to 'Active' will be displayed."))

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        translate = ('description', )
        ordering = ['position']

    def __unicode__(self):
        return self.name

class ImageSlider(models.Model):
    """
    Images Sliders Management
    """
    __metaclass__ = TransMeta
    
    name = models.CharField(_('name'),max_length=100)
    slug = models.SlugField(_('slug'),)
    description = models.TextField(_('description'),blank=True, null=True)

    class Meta:
        verbose_name = _('Slider Box')
        verbose_name_plural = _('Sliders Boxes')

    def __unicode__(self):
        return "%s" % self.name

    def save(self):
        """
        Re-order all items at from 10 upwards, at intervals of 10.
        """
        super(ImageSlider, self).save()

        current = 10
        for item in ImageSliderItem.objects.filter(slider=self).order_by('order'):
            item.order = current
            item.save()
            current += 10
 
class ImageSliderItem(models.Model):
    """
    Images Sliders Items
    """
    __metaclass__ = TransMeta

    slider = models.ForeignKey(ImageSlider)
    slimg = models.ImageField(_('image'), upload_to='sliders', help_text=_("Check Documentation about size image"))
    title = models.CharField(_('title'),max_length=100)
    link_url = models.CharField(_('link url'),max_length=100, help_text=_('URL or URI, eg /about/ or http://foo.com/'))
    order = models.IntegerField(_('order'),)
    status = models.IntegerField(_('status'), choices=enums.CMS_STATUS_CHOICES, default=enums.STATUS_ACTIVE, help_text=_("Only items with their status set to 'Active' will be displayed."))

    class Meta:
        verbose_name = _('Sliders Image')
        verbose_name_plural = _('Sliders Images')
        translate = ('title', 'link_url', 'slimg')
        ordering = ['order']

    def __unicode__(self):
        return "%s %s. %s" % (self.slider.slug, self.order, self.title)
