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
from catalog.models import *
from datetime import datetime
from . import models

class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'parent',
        'name',
        'position',
        'slug',
        'fslug',
    )
    search_fields = [
        "name_en",
        ]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductProductInline(admin.StackedInline):
    model = models.ProductProduct

class ProductTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'name_en',
    )
    search_fields = [
        "name_en",
    ]
    extra = 0
#    list_filter = ["status"]
    inlines = [ProductProductInline]

admin.site.register(ProductTemplate, ProductTemplateAdmin)

class ProductImagesAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'product',
    )
    search_fields = [
        "name",
        "product__code",
    ]
    extra = 0
#    list_filter = ["status"]

admin.site.register(ProductImages, ProductImagesAdmin)

class ProductHomeAdmin(admin.ModelAdmin):
    """Product Home Admin"""

    list_display = (
        'tplproduct',
        'status',
        'order',
    )
    search_fields = ["tplproduct"]

admin.site.register(ProductHome, ProductHomeAdmin)

class ProductRecommendedAdmin(admin.ModelAdmin):
    """Product Recommended Admin"""

    list_display = (
        'tplproduct',
        'status',
        'order',
    )
    search_fields = ["tplproduct"]

admin.site.register(ProductRecommended, ProductRecommendedAdmin)

class ProductOfferAdmin(admin.ModelAdmin):
    """Product Offer Admin"""

    list_display = (
        'tplproduct',
        'status',
        'order',
    )
    search_fields = ["tplproduct"]

admin.site.register(ProductOffer, ProductOfferAdmin)

class ResManufacturerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug',
        'active',
    )
    search_fields = [
        "name",
        ]
    prepopulated_fields = {
        'slug': ('name',),
    }
    extra = 0
#    list_filter = ["status"]

admin.site.register(ResManufacturer, ResManufacturerAdmin)

class AttributeSearchPriceInline(admin.TabularInline):
    """
    Attribute Search Prices Management Admin
    """

    model = models.AttributeSearchPrice
    extra = 3

class AttributeSearchItemInline(admin.TabularInline):
    """
    Attribute Search Items Management Admin
    """

    model = models.AttributeSearchItem
    extra = 3

class AttributeSearchAdmin(admin.ModelAdmin):
    """
    Attribute Search Management Admin
    """

    list_display = (
        'name',
        'active',
    )
    search_fields = ["name"]
    inlines = [AttributeSearchItemInline, AttributeSearchPriceInline]

admin.site.register(AttributeSearch,AttributeSearchAdmin)
