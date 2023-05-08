from django.urls import path

from blog.views import (add_blog, blog, blogs, comment_del, comment_update,
                        custom_404_page, del_blog, reply_page, search,
                        update_blog)

urlpatterns = [
    path('', blogs, name='blogs'),
    path('show_404_page', custom_404_page, name='custom_404_page'),
    path('add/', add_blog, name='add_blog'),
    path('update/<slug:slug>/', update_blog, name='update_blog'),
    path('del/<slug:slug>/', del_blog, name='del_blog'),
    path('search/', search, name='search'),
    path('search/<int:page_number>', search, name='paginator_search'),
    path('<int:page_number>', blogs, name='paginator'),
    path('category/<int:category_id>/', blogs, name='category'),
    path('author/<int:author_id>/', blogs, name='author'),
    path('comment/reply/', reply_page, name='reply'),
    path('comment/edit/<int:comment_id>', comment_update, name='comment_update'),
    path('comment/del/<int:comment_id>', comment_del, name='comment_del'),
    path('<slug:slug>/', blog, name='blog'),
    path('<slug:slug>/<int:page_number>/', blog, name='paginator_blog'),

]
