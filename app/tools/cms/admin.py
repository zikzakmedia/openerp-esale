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

from django.contrib import admin

from tools.cms.models import *
from . import models

class SiteConfigurationAdmin(admin.ModelAdmin):
    """
    Site Configuration Management Admin
    """

    list_display = (
        'name',
        'domain',
    )
    search_fields = ["name","domain"]
    
admin.site.register(SiteConfiguration,SiteConfigurationAdmin)

class MenuItemInline(admin.TabularInline):
    """
    Menu Items Management Admin
    """

    model = models.MenuItem

class MenuAdmin(admin.ModelAdmin):
    """
    Menu Management Admin
    """

    list_display = (
        'name',
        'slug',
        'base_url'
    )
    search_fields = ["name", "base_url"]
    prepopulated_fields = {
        'slug': ('name',),
    }
    inlines = [MenuItemInline]
    
admin.site.register(Menu,MenuAdmin)

class ModulesAdmin(admin.ModelAdmin):
    """
    Modules Management Admin
    """

    list_display = (
        'name',
        'position',
        'status'
    )

    class Media:
        js = (
            '/static/js/ckeditor/ckeditor.js',
            '/static/js/ckeditor.js',
        )

admin.site.register(Modules,ModulesAdmin)

class ImageSliderInline(admin.TabularInline):
    """
    Image Slider Items Management Admin
    """

    model = models.ImageSliderItem
    extra = 3
    max_num = 6

class ImageSliderAdmin(admin.ModelAdmin):
    """
    Image Slider Management Admin
    """

    list_display = (
        'name',
        'slug',
    )
    search_fields = ["name"]
    prepopulated_fields = {
        'slug': ('name',),
    }
    inlines = [ImageSliderInline]

admin.site.register(ImageSlider,ImageSliderAdmin)
