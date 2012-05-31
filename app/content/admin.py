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
from content.models import *
from datetime import datetime

class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['name_en','name_es','slug_en','slug_es']}),
        ('Description', {'fields': ['description_en','description_es']}),
        ('SEO', {'fields': ['metadesc_en','metadesc_es','metakey_en','metakey_es']}),
        ('Page', {'fields': ['status','sort_order','template']}),
    ]
    list_display = (
        'name',
        'slug',
        'sort_order',
        'created_by',
        'created_on',
        'updated_by',
        'updated_on',
        'status'
    )
    search_fields = [
        "name_en",
        "description_en",
        "name_es",
        "description_es",
        ]
    list_filter = ["status"]
    prepopulated_fields = {
        'slug_en': ('name_en',),
        'slug_es': ('name_es',),
    }

    class Media:
        js = (
            '/static/js/ckeditor/ckeditor.js',
            '/static/js/ckeditor.js',
        )

    def save_model(self, request, obj, form, change): 
        """
        Overrided because I want to also set who created this instance.
        """
        instance = form.save(commit=False)
        if instance.id is None:
            new = True
            instance.created_by = request.user
        instance.updated_by = request.user
        instance.save()
        return instance

admin.site.register(Content, ContentAdmin)
