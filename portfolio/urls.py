from django.urls import path
from portfolio.views import portfolios, portfolio

urlpatterns = [
    path('', portfolios, name='portfolios'),
    path('<int:portfolio_id>', portfolio, name='portfolio'),
    path('<slug:category_slug>', portfolios, name='filter_category'),
]