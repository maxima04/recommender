from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('survey/', views.survey, name="survey"),
    path('login/', views.login, name="login"),
    #path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('sentimentChart/', views.sentimentPage, name="sentiment"), 
    path('likertChart/', views.likertPage, name="likert"),
    path('aspectChart/', views.aspectPage, name="aspect"), 

    #Summary pages
    path('likertSummary/', views.likertSummary, name="summaryLikert"), 
    path('sentimentSummary/', views.sentimentSummary, name="summarySentiment"), 
    path('aspectSummary/', views.aspectSummary, name="summaryAspect"),

    path('summaryPage/', views.summaryPage, name="summary"),

    #for admin
    path('dashboard/', views.dashboard, name="dashboard"),

    path('logout/', views.logout, name="logout"),



]
