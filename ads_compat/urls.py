from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abs/<bibcode>', views.abstract, name='abstract'),
]