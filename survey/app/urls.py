from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('survey/', views.survey, name="survey"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('sentimentChart/', views.sentimentPage, name="sentiment"), 
    path('likertChart/', views.likertPage, name="likert"),
    path('aspectChart/', views.aspectPage, name="aspect"), 
    path('thankyou/', views.submitted, name="submitted"),


]
