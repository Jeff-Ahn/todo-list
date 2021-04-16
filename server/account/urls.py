from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.DefaultRouter()

router.register("account", viewset=views.AccountViewSet, basename="account")
router.register("person", viewset=views.PersonViewSet, basename="person")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginAPIView.as_view(), name='login'),
    path("logout/", views.LogoutAPIView.as_view()),
]
