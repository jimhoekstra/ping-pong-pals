from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('scoreboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('leagues/', include('leagues.urls')),
    path('admin/', admin.site.urls),
]
