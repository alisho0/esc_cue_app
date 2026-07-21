from django.urls import path

from .views import dashboard

app_name = 'panel'

urlpatterns = [
    path('', dashboard, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
]
