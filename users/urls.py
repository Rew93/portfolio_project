from django.urls import path

from users.views import (activate, login_register, logout, new_password,
                         password_change, password_reset,
                         password_reset_confirm, profile)

urlpatterns = [
    path('login_register', login_register, name='login_register'),
    path('logout', logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
    path('password_change', password_change, name='password_change'),
    path('password_reset', password_reset, name='password_reset'),
    path('new_password', new_password, name='new_password'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
