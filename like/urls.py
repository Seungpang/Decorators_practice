from django.urls import path
from . import views

urlpatterns = [
    path('like/', views.api_like),
    path('unlike/', views.api_unlike),
]
