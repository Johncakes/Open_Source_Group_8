from django.urls import path
from config.views import index

urlpatterns = [
    path('', index, name='index'),
]
