from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all', views.all_links, name='allLinks'),
    path('create', views.create, name='create'),
    path('<str:short_link>', views.redirect, name='redirect'),
    path('remove/<int:link_id>', views.remove, name='remove'),
]