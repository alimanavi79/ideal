from django.contrib import admin
from . import models
from .models import TechnicalSpecification


# Register your models here.

class SpecificationKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'category']

class TechnicalSpecificationInline(admin.TabularInline):
    model = TechnicalSpecification
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'discounted_price', 'inventory', 'is_active', 'is_delete']
    list_editable = ['price', 'discounted_price', 'is_active', 'inventory']
    inlines = [TechnicalSpecificationInline]


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_date', 'end_date','discount_percentage']
    list_editable = [ 'start_date', 'end_date', 'discount_percentage']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.SpecificationKey, SpecificationKeyAdmin)
admin.site.register(TechnicalSpecification)
admin.site.register(models.DiscountCode, DiscountCodeAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
