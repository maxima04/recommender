from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('survey/', views.survey, name="survey"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('sentimentChart/', views.sentimentPage, name="sentiment"), 

]
