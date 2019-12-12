from django.urls import path

from .views import *


urlpatterns = [
    path('button/', GetList.as_view())
]
