from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register('user', viewset=views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view())
]