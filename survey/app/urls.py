from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('survey/', views.survey, name="survey"),
    path('about/', views.about, name="about"),
    path('sentimentChart/', views.sentimentPage, name="sentiment"), 

]
