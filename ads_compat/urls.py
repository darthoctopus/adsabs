from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abs/<bibcode>', views.abstract, name='abstract'),
    path('search/<qstring>', views.qsearch, name='qsearch'),
    path('search', views.qsearch, name='qsearch'),
    path('search/', views.qsearch, name='qsearch'),
]