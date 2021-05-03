from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('survey/', views.survey),
    path('about/', views.about),

]
