from django.shortcuts import render
from django.http import HttpResponse
from app.forms import SurveyForm, LikertForm, OpinionForm
from .models import Surveyquestions

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