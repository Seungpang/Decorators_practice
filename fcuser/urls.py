from django.urls import path
from . import views

urlpatterns = [
    path('validation/', views.validation),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('', views.PublisherList.as_view()),
]
