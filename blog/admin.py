from django.contrib import admin

from blog.models import BlogModel, CategoryModel, CommentsModel


# Register your models here.
@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug',)
    list_display = ('name',)


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    filter_horizontal = ('category',)
    list_filter = ('category', 'author')
    ordering = ('author',)
    fields = ('title', 'author', 'text_story', 'image', 'image_2', 'image_popular_blog', 'video', 'category', 'slug')
    list_per_page = 10


@admin.register(CommentsModel)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog',)
    list_filter = ('author', 'date_created')
    fields = ('author', 'text_comment', 'blog', 'parent')
