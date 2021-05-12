from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from app.forms import SurveyForm, LikertForm, OpinionForm, RegistrationForm, LoginForm, TitleForm
from .models import Surveyquestions, User
from .controller import *
import json
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import urllib
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
COMMONS_DIR = os.path.join(BASE_DIR, 'app/commons')
LIKERT_SURVEY_DIR = os.path.join(COMMONS_DIR,'likert_survey.csv')
OPINION_SURVEY_DIR = os.path.join(COMMONS_DIR,'opinion_survey.csv')



col_df = pd.read_csv(LIKERT_SURVEY_DIR)
op_col = pd.read_csv(OPINION_SURVEY_DIR)
column_name = [col for col in col_df.columns]
opinion_column = [col for col in op_col.columns]

import pickle

# Create your views here.

def home(request):
    aspect, comment = getAspect()

    ASPECT_DICT_DIR = os.path.join(COMMONS_DIR,'aspect.pkl')
    COMMENT_DICT_DIR = os.path.join(COMMONS_DIR,'comment.pkl')

    with open(ASPECT_DICT_DIR, "wb") as tf:
        pickle.dump(aspect,tf)

    with open(COMMENT_DICT_DIR, "wb") as td:
        pickle.dump(comment,td)

    SENTIMENT_DICT_DIR = os.path.join(COMMONS_DIR,'sentiment.pkl')

    sentiment, _ndf = calculateSentiment()

    with open(SENTIMENT_DICT_DIR, "wb") as tf:
        pickle.dump(_ndf,tf)

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

    ASPECT_DICT_DIR = os.path.join(COMMONS_DIR,'aspect.pkl')
    COMMENT_DICT_DIR = os.path.join(COMMONS_DIR,'comment.pkl')
    SENTIMENT_DICT_DIR = os.path.join(COMMONS_DIR,'sentiment.pkl')


    with open(ASPECT_DICT_DIR, "rb") as tf:
        aspect = pickle.load(tf)

    with open(COMMENT_DICT_DIR, "rb") as tb:
        comment = pickle.load(tb)

    with open(SENTIMENT_DICT_DIR, "rb") as ts:
        sent = pickle.load(ts)
    
    selected_title = 'I can easily log-in and log-out my Canvas account. '
    form = TitleForm()
    if request.method == 'POST':
        form = TitleForm(request.POST)
      
        if form.is_valid():
            selected_title = request.POST.get('title')


    

    #print(list(comment[selected].values()))
    
    
    sentiment = list(sent[selected_title].values())

    acad_filter = ['subject','teacher','teach','faculty',
                    'professor','school','system','learning',
                    'modules','module','teaching'
                    'assignments','assignment','knowledge','activities']

    ito_filter = ['system','internet','connection',
                    'slow','laboratory','access',
                    'equipment']

    itbl_filter = ['canvas','design','slow','platform',
                    'application','access','survey',
                    'modules','modules','log']

    
    acad_dict = {}
    ito_dict = {}
    itbl_dict = {}

    print(selected_title)
    print(aspect[selected_title])
    for i, k in aspect[selected_title].items():

        acad_results = findAc(acad_filter, k)
        ito_results = findAc(ito_filter, k)
        itbl_results = findAc(itbl_filter, k)

        
        if len(acad_results) != 0:
            acad_dict[i] = k

        if len(ito_results) != 0:
            ito_dict[i] = k

        if len(itbl_results) != 0:
            itbl_dict[i] = k
        else:
            None

    filterd_acad_comment = {key: value for key, value in comment[selected_title].items() if key in acad_dict.keys()}
    filterd_ito_comment = {key: value for key, value in comment[selected_title].items() if key in ito_dict.keys()}
    filterd_itbl_comment = {key: value for key, value in comment[selected_title].items() if key in itbl_dict.keys()}

    print(acad_dict)
    print(filterd_acad_comment)


    word = [i for i in aspect[selected_title].values()]

    comment = ''

    for i in aspect[selected_title].values():
        comment += " ".join(i)+" "

    wordcloud = WordCloud(background_color="white",width=1000,height=1000, max_words=10).generate(comment)
    plt.figure(figsize=(3,3))
    plt.imshow(wordcloud, interpolation="bilinear", aspect='auto')
    plt.axis('off')

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    context = {
        'column_name':column_name,
        'uri':uri,

        'acad_dict':acad_dict,
        'ito_dict':ito_dict,
        'itbl_dict':itbl_dict,

        'sentiment':sentiment,

        'filterd_acad_comment':filterd_acad_comment,
        'filterd_ito_comment':filterd_ito_comment,
        'filterd_itbl_comment':filterd_itbl_comment,

        'form':form,

        
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