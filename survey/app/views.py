from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from app.forms import SurveyForm, LikertForm, OpinionForm, RegistrationForm, LoginForm
from .models import Surveyquestions, User
from .controller import *

# Create your views here.

def home(request):
    return render(request, 'app/dashboard.html')

def survey(request):

    if request.method == 'POST':


        surveyform = SurveyForm(request.POST)
        likertForm = LikertForm(request.POST)
        opinionForm = OpinionForm(request.POST)

        if surveyform.is_valid() and likertForm.is_valid() and opinionForm.is_valid():
            print('Form is valid!')

            '''
            !!! Note !!!
            Try to print a1 variable if form.cleaned_data.get() is working accordingly
            you can remove controller.py if it takes too long to load
            '''
            
            #Get likert form data
            a1 = likertForm.cleaned_data.get('a1')
            a2 = likertForm.cleaned_data.get('a2')
            #Please contiue until finished

            likert_data = [a1,a2] ## input all
            uploadDataLikert(likert_data) ## upload form data to csv

            #Get opinion form data, do not include subject name
            a1 = surveyform.cleaned_data.get('a1')
            a2 = surveyform.cleaned_data.get('a2')
            #Please contiue until finished

            survey_data = [a1,a2] ## input all variables
            uploadDataSentiment(survey_data) ## upload form data to csv

            #Get opinion form data
            e1 = opinionForm.cleaned_data.get('e1')
            e2 = opinionForm.cleaned_data.get('e2')
            e3 = opinionForm.cleaned_data.get('e4')

            ### No function for here yet
            opinion_data = [e1,e2,e3] ## input all variables
            

            return render(request, 'app/dashboard.html')
            
    # if a GET (or any other method) we'll create a blank form
    else:
        surveyform = SurveyForm()
        likertform = LikertForm()
        opinionform = OpinionForm()

        questions = Surveyquestions.objects.all()

        zipped_data = zip(likertform, surveyform)
        survey = list(zipped_data)

        context = {
            'form': survey,
            'questions': questions,
            'opinionform': opinionform,
        }

        return render(request, 'app/survey.html', context)

def about(request):
    return render(request, 'app/about.html')


def likertPage(request):

    likert = countLikert()
    likert = json.dumps(likert)
    context = {
        'column_name':column_name,
        'likert':likert,
        
        }

    return render(request, 'likertChart.html', context)

def sentimentPage(request):

    sentiment = calculateSentiment()

    context = {
        'sentiment':sentiment,
        'column_name':column_name,
        
        }

    return render(request, 'app/sentimentChart.html', context)

def aspectPage(request):

    _aspect, _comment = getAspect()

    context = {
        'column_name':column_name,
        'aspect':aspect
    }

    return render(request, 'app/aspectChart.html', context)

def login(request):

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            userpass = loginForm.cleaned_data['password']

            if User.objects.filter(username=username, password=userpass):
                context = {
                    'username': username
                }

                messages.success(request, "You have login successfully!")
                return redirect('/home', context)

        messages.error(request, "Wrong Username/Password!")
        return redirect('/login')

    else:
        loginForm = LoginForm()

        context = {
            'loginForm': loginForm,
        }

        return render(request, 'app/login.html', context)

def register(request):


    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)

        if registrationForm.is_valid():
            name = registrationForm.cleaned_data['name']
            uname = registrationForm.cleaned_data['username']
            pword = registrationForm.cleaned_data['password']

            userdata = User(name=name, username=uname, password=pword, is_user=1, is_admin=0, is_itbl=0, is_ito=0)
            userdata.save()

            context = {
                'name': name,
                'uname': uname,
            }
            return redirect('/home', context)
    else:
        registrationForm = RegistrationForm()

        context = {
            'registrationForm': registrationForm,
        }

        return render(request, 'app/register.html', context)