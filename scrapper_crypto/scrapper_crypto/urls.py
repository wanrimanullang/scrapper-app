from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrapper_api/', include('scrapper_api.urls')),
]
