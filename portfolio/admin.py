from django.contrib import admin

from portfolio.models import PortfolioModel


# Register your models here.
@admin.register(PortfolioModel)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_create',)
    filter_horizontal = ('category',)
    fields = ('author', 'description', 'development', 'design', 'photography', 'image', 'image_2', 'image_3', 'video',
              'client', 'date_create', 'link_on_project', 'category')
    ordering = ('date_create',)
    list_filter = ('category',)

