from django.urls import path

from .views import *


urlpatterns = [
    path('button/', ButtonView.as_view()),
    path('text/', TextView.as_view()),
]
