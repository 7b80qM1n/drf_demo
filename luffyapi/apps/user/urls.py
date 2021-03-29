from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('', views.LoginView, 'login')
router.register('', views.SendSmsView, 'send')
router.register('register', views.RegisterView, 'register')
urlpatterns = [
    path('', include(router.urls))
]
