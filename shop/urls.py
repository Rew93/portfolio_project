from django.urls import path

from shop.views import products, product, delete_review, checkout, add_checkout, remove_checkout, update_checkout

urlpatterns = [
    path('', products, name='products'),
    path('page/<int:page_number>', products, name='paginator_product'),
    path('<slug:slug_product>', product, name='product'),
    path('<slug:slug_product>/edit<int:id>', product, name='edit_product'),
    path('del_review/<int:id>', delete_review, name='delete_review'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/add/<str:product_slug>', add_checkout, name='add_checkout'),
    path('checkout/remove/<int:checkout_id>', remove_checkout, name='remove_checkout'),
    path('update-checkout/', update_checkout)
]
