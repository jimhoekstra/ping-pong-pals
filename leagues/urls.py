from django.urls import path
from . import views


urlpatterns = [
    path('overview', views.overview, name='leagues-overview'),
    path('new', views.new_league_page, name='new-league-page'),
    path('create', views.create_new_league, name='create-new-league'),
    path('submit-join-request', views.submit_join_request, name='submit-join-request'),
    path('activate-league', views.activate_league, name='activate-league'),
]
