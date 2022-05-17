from django.contrib import admin
from django.urls import path, include

from linkshortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:short_link>', views.redirect, name='redirect'),
    path('links/', include('linkshortener.urls')),
]
