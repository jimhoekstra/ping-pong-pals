from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_page, name='login-page'),
    path('login-user', views.login_user, name='login-user'),
    path('logout-user', views.logout_user, name='logout-user'),
    path('create-account', views.create_account, name='create-account'),
    path('overview', views.overview, name='account-overview'),
    path('update-profile-name', views.update_profile_name, name='update-profile-name'),
    path('update-password', views.update_password, name='update-password'),
]
