from . import views
from django.urls import path
from django.shortcuts import redirect

app_name = 'main_app'
urlpatterns = [
    path('', lambda request: redirect('/search/')),
    path('search/', views.index, name='index'),
]