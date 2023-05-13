from django.urls import path
from portfolio.views import portfolios

urlpatterns = [
    path('', portfolios, name='portfolios'),
]