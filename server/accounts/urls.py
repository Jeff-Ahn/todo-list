from .views import sign_up
from django.urls import path

urlpatterns = [
    path('api/signup', sign_up)
]