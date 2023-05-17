from django.contrib import admin

from shop.models import ProductModel, ReviewModel, BrandModel, ImagesModel, CategoryProductModel, SizeGridModel, \
    ProductSizeModel

# Register your models here.
admin.site.register(ImagesModel)
admin.site.register(SizeGridModel)


@admin.register(ProductSizeModel)
class ProductSizeAdmin(admin.ModelAdmin):
    fields = ('product', 'size', 'count')
    ordering = ('product', 'size')
    list_filter = ('product', 'size', 'count')


@admin.register(CategoryProductModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'parent')


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'slug', 'description', 'price', 'category', 'sizes', 'gender', 'compositions', 'color', 'brand',
        'images')
    list_filter = ('name', 'brand', 'price', 'category',)
    list_display = ('name', 'price')
    list_per_page = 10
    filter_horizontal = ('category', 'sizes')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product',)
    list_filter = ('author', 'date_created')
    fields = ('author', 'rating', 'text_comment', 'product', 'parent')


@admin.register(BrandModel)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug')
