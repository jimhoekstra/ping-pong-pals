from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_page, name='login-page'),
    path('login-user', views.login_user, name='login-user'),
    path('logout-user', views.logout_user, name='logout-user'),
]
