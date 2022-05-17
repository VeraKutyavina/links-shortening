from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<str:short_link>', views.redirect, name='redirect'),
    path('', views.index, name='index'),
]