from django.contrib import admin
from django.urls import path, include

from linkshortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('linkshortener.urls')),
]
