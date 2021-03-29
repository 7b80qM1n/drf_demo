from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('pay', views.PayView, 'pay')
urlpatterns = [
    path('', include(router.urls)),
    path('success/', views.SuccessView.as_view()),
]
