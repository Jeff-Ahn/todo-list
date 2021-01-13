from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register('user', viewset=views.UserViewSet)
router.register('login', viewset=views.LoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]