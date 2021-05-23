from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from app.forms import LikertSurveyForm, RegistrationForm, LoginForm, TitleForm
from .models import Surveyquestions, User, Likert, Opinion, Survey
from django.contrib.auth import authenticate, login, logout
from .controller import *
import json
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import urllib
import csv
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

#class for user variables

class UserVariables:
    userId = 0
    userName = ""
    userRole = ""

def user_auth():
    # check if user logged in if not, redirect to login page
    user_id = UserVariables.userId
    if user_id == 0:
        redirectUser = True
        return redirectUser

def login_user(username, password, request):
    if User.objects.filter(username=username, password=password):
        userIsUser = 0
        userIsItbl = 0
        userIsIto = 0
        userIsAcad = 0

        getUser = User.objects.filter(username=username, password=password)
        for userInfo in getUser:
            UserVariables.userId = userInfo.id
            UserVariables.userName = userInfo.username
            userIsUser = userInfo.is_user
            userIsItbl = userInfo.is_itbl
            userIsIto = userInfo.is_ito
            userIsAcad = userInfo.is_acad

        request.session['userIsAcad'] = userIsAcad
        request.session['userIsItbl'] = userIsItbl
        request.session['userIsIto'] = userIsIto

        if userIsUser == 1:
            UserVariables.userRole = "user"
            page = "/survey"
        elif userIsItbl == 1:
            UserVariables.userRole = "itbl"
            page = "/summaryPage"
        elif userIsIto == 1:
            UserVariables.userRole = "acads"
            page = "/summaryPage"
        elif userIsAcad == 1:
            UserVariables.userRole = "ito"
            page = "/summaryPage"
        else:
            page = "/login"
    else:
        page = "/login"

    return page
# Create your views here.

def home(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')
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
    #check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')


    if request.method == 'POST':

        likertSurvey = LikertSurveyForm(request.POST)

        if likertSurvey.is_valid():

            # Likert data
            courseName = likertSurvey.cleaned_data['course_name']
            a1 = likertSurvey.cleaned_data['a1']
            a2 = likertSurvey.cleaned_data['a2']
            a3 = likertSurvey.cleaned_data['a3']
            a4 = likertSurvey.cleaned_data['a4']
            a5 = likertSurvey.cleaned_data['a5']
            a6 = likertSurvey.cleaned_data['a6']
            a7 = likertSurvey.cleaned_data['a7']
            a8 = likertSurvey.cleaned_data['a8']
            a9 = likertSurvey.cleaned_data['a9']
            a10 = likertSurvey.cleaned_data['a10']
            a11 = likertSurvey.cleaned_data['a11']
            a12 = likertSurvey.cleaned_data['a12']
            a13 = likertSurvey.cleaned_data['a13']
            a14 = likertSurvey.cleaned_data['a14']
            a15 = likertSurvey.cleaned_data['a15']
            a16 = likertSurvey.cleaned_data['a16']
            a17 = likertSurvey.cleaned_data['a17']

            i1 = likertSurvey.cleaned_data['i1']
            i2 = likertSurvey.cleaned_data['i2']
            i3 = likertSurvey.cleaned_data['i3']
            ac1 = likertSurvey.cleaned_data['ac1']
            ac2 = likertSurvey.cleaned_data['ac3']
            ac3 = likertSurvey.cleaned_data['ac3']
            ac4 = likertSurvey.cleaned_data['ac4']
            ac5 = likertSurvey.cleaned_data['ac1']
            ac6 = likertSurvey.cleaned_data['ac3']
            ac7 = likertSurvey.cleaned_data['ac3']
            ac8 = likertSurvey.cleaned_data['ac4']


            likert_data = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15, a16,a17,i1,i2,i3,ac1,ac2,ac3,ac4,ac5,ac6,ac7,ac8]
            uploadDataLikert(likert_data) ## upload form data to csv

            #Get opinion form data, do not include subject name
            sa1 = likertSurvey.cleaned_data['sa1']
            sa2 = likertSurvey.cleaned_data['sa2']
            sa3 = likertSurvey.cleaned_data['sa3']
            sa4 = likertSurvey.cleaned_data['sa4']
            sa5 = likertSurvey.cleaned_data['sa5']
            sa6 = likertSurvey.cleaned_data['sa6']
            sa7 = likertSurvey.cleaned_data['sa7']
            sa8 = likertSurvey.cleaned_data['sa8']
            sa9 = likertSurvey.cleaned_data['sa9']
            sa10 = likertSurvey.cleaned_data['sa10']
            sa11 = likertSurvey.cleaned_data['sa11']
            sa12 = likertSurvey.cleaned_data['sa12']
            sa13 = likertSurvey.cleaned_data['sa13']
            sa14 = likertSurvey.cleaned_data['sa14']

            si1 = likertSurvey.cleaned_data['si1']
            si2 = likertSurvey.cleaned_data['si2']
            si3 = likertSurvey.cleaned_data['si3']
            sac1 = likertSurvey.cleaned_data['sac1']
            sac2 = likertSurvey.cleaned_data['sac3']
            sac3 = likertSurvey.cleaned_data['sac3']
            sac4 = likertSurvey.cleaned_data['sac4']


            survey_data = [sa1,sa2,sa3,sa4,sa5,sa6,sa7,sa8,sa9,sa10,sa11,sa12,sa13,sa14,si1,si2,si3,sac1,sac2,sac3,sac4]
            uploadDataSentiment(survey_data) ## upload form data to csv

            #Get opinion form data
            e1 = likertSurvey.cleaned_data['e1']
            e2 = likertSurvey.cleaned_data['e2']
            e3 = likertSurvey.cleaned_data['e3']

            ### No function for here yet
            opinion_data = [e1,e2,e3]

            timeStamp = timezone.make_naive(timezone.now())
            user_id=UserVariables.userId

            #save data to database
            likertData = Likert(user_id=user_id, course_name=courseName, timestamp=timeStamp, a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13, a14=a14, a15=a15, a16=a16, a17=a17, i1=i1, i2=i2, i3=i3, ac1=ac1, ac2=ac2, ac3=ac3, ac4=ac4, ac5=ac5, ac6=ac6, ac7=ac7, ac8=ac8)
            likertData.save()

            surveyData = Survey(user_id=user_id, course_name=courseName, timestamp=timeStamp, a1=sa1, a2=sa2, a3=sa3, a4=sa4, a5=sa5, a6=sa6, a7=sa7, a8=sa8, a9=sa9, a10=sa10, a11=sa11, a12=sa12, a13=sa13, a14=sa14, i1=si1, i2=si2, i3=si3, ac1=sac1, ac2=sac2, ac3=sac3, ac4=sac4)
            surveyData.save()

            opinionData = Opinion(user_id=user_id, e1=e2, e2=e2, e3=e3)
            opinionData.save()

            print(likert_data)
            print(survey_data)
            print(opinion_data)

            messages.success(request, "Submitted successfully!")
            return redirect('/survey')

        else:
            messages.error(request, "Try Again!")
            return redirect('/survey')
            
    # if a GET (or any other method) we'll create a blank form
    else:
        likertSurvey = LikertSurveyForm()
        questions = Surveyquestions.objects.all()

        currentPage = "/survey/"
        context = {
            'questions': questions,
            'form': likertSurvey,
            'currentPage': currentPage,
            'role': UserVariables.userRole
        }
        return render(request, 'app/survey.html', context)


def likertPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')


    likert, dataframe, _dict = countLikert()

    likert = json.dumps(likert)
    currentPage = "/likertChart/"

    context = {
        'column_name':column_name,
        'likert':likert,
        'currentPage': currentPage,
        'role': UserVariables.userRole,
        
    }

    return render(request, 'app/likertChart.html', context)

def likertSummary(request):

    _likert, dataframe, _dict = countLikert()

    context = {
        'dataframe':dataframe,
        '_dict':_dict

    }

    return render(request, 'app/likertSummary.html', context)

def sentimentSummary(request):

    thisSent,comp = calculateSentiment()


    context = {
        'thisSent':thisSent,
        'comp':comp

    }

    return render(request, 'app/sentimentSummary.html', context)

def aspectSummary(request):

    ASPECT_DICT_DIR = os.path.join(COMMONS_DIR,'aspect.pkl')

    with open(ASPECT_DICT_DIR, "rb") as tf:
        aspect = pickle.load(tf)

 
    sent, comp = calculateSentiment()
    
    acad_filter = ['subject','teacher','teach','faculty',
                    'professor','school','system','learning',
                    'modules','module','teaching'
                    'assignments','assignment','knowledge','activities']

    ito_filter = ['system','internet','connection',
                    'slow','laboratory','access',
                    'equipment']

    itbl_filter = ['canvas','design','slow','platform',
                    'application','survey',
                    'modules','modules','log']


    sent_value = [i for i in sent.values()]

    AcadSummary = summarized_aspect(acad_filter,sent_value,aspect)
    ItoSummary = summarized_aspect(ito_filter,sent_value,aspect)
    ItblSummary = summarized_aspect(itbl_filter,sent_value,aspect)

    Acaddept = [i['Dept_aspect'] for i in AcadSummary]
    Itodept = [i['Dept_aspect'] for i in ItoSummary]
    Itbldept = [i['Dept_aspect'] for i in ItblSummary]


    Acadcomment = ''
    for i in Acaddept:
        Acadcomment += " ".join(i)+" "

    Itocomment = ''
    for i in Itodept:
        Itocomment += " ".join(i)+" "

    Itblcomment = ''
    for i in Itbldept:
        Itblcomment += " ".join(i)+" "


    acadWordCloud = generateWordcloud(Acadcomment)
    ItoWordCloud = generateWordcloud(Itocomment)
    ItblWordCloud = generateWordcloud(Itblcomment)


    userIsAcad = request.session['userIsAcad']
    userIsItbl = request.session['userIsItbl']
    userIsIto = request.session['userIsIto']


    context = {

        'AcadSummary':AcadSummary,
        'ItoSummary':ItoSummary,
        'ItblSummary':ItblSummary,

        'userIsAcad':userIsAcad,
        'userIsItbl':userIsItbl,
        'userIsIto':userIsIto,

        'acadWordCloud':acadWordCloud,
        'ItoWordCloud':ItoWordCloud,
        'ItblWordCloud':ItblWordCloud,

        
    }

    return render(request, 'app/aspectSummary.html', context)

def sentimentPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')

    sentiment,comp = calculateSentiment()
    print(comp)
    currentPage = "/sentimentChart/"
    context = {
        'sentiment':sentiment,
        'column_name':column_name,
        'currentPage': currentPage,
        'role': UserVariables.userRole,
        'comp':comp
        }

    return render(request, 'app/sentimentChart.html', context)

def aspectPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')

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
    
    
    sentiment = sent[selected_title]


    acad_filter = ['subject','teacher','teach','faculty',
                    'professor','school','system','learning',
                    'modules','module','teaching'
                    'assignments','assignment','knowledge','activities']

    ito_filter = ['system','internet','connection',
                    'slow','laboratory','access',
                    'equipment']

    itbl_filter = ['canvas','design','slow','platform',
                    'application','survey',
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

    acadPlan = actionPlan(filterd_acad_comment,sentiment)
    itoPlan = actionPlan(filterd_ito_comment,sentiment)
    itblPlan = actionPlan(filterd_itbl_comment,sentiment)


    userIsAcad = request.session['userIsAcad']
    userIsItbl = request.session['userIsItbl']
    userIsIto = request.session['userIsIto']

    currentPage = "/aspect/"

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

        'acadPlan':acadPlan,
        'itoPlan':itoPlan,
        'itblPlan':itblPlan,

        'userIsAcad':userIsAcad,
        'userIsItbl':userIsItbl,
        'userIsIto':userIsIto,


        'form':form,
        'currentPage': currentPage,
        'role': UserVariables.userRole
    }
    return render(request, 'app/aspectChart.html', context)

def login(request):

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            userpass = loginForm.cleaned_data['password']

            redirectToPage = login_user(username, userpass, request)

            if redirectToPage == "/login":
                messages.error(request, "Wrong username/password!")

            return redirect(redirectToPage)

        else:
            messages.error(request, "Wrong Username/Password!")
            return redirect('/login')

    else:
        loginForm = LoginForm()
        currentPage = "/login/"
        context = {
            'loginForm': loginForm,
            'currentPage': currentPage,
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

            redirectToPage = login_user(name, pword)

            return redirect(redirectToPage)
        else:
            messages.error(request, "Try again!")
            return redirect('/register')
    else:
        registrationForm = RegistrationForm()
        currentPage = "/register/"
        context = {
            'registrationForm': registrationForm,
            'currentPage': currentPage,
        }
        return render(request, 'app/register.html', context)

def dashboard(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')

    context = {
        'role': UserVariables.userRole
    }
    return render(request, 'app/aspectChart.html', context)

def logout(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')
    UserVariables.userId = 0

    messages.success(request, "Successfully logout!")
    return redirect('/login')

def summaryPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        return redirect('/login')


    #aspect
    def summaryAspect():
        ASPECT_DICT_DIR = os.path.join(COMMONS_DIR, 'aspect.pkl')

        with open(ASPECT_DICT_DIR, "rb") as tf:
            aspect = pickle.load(tf)

        sent, comp = calculateSentiment()

        acad_filter = ['subject', 'teacher', 'teach', 'faculty',
                       'professor', 'school', 'system', 'learning',
                       'modules', 'module', 'teaching'
                                            'assignments', 'assignment', 'knowledge', 'activities']

        ito_filter = ['system', 'internet', 'connection',
                      'slow', 'laboratory', 'access',
                      'equipment']

        itbl_filter = ['canvas', 'design', 'slow', 'platform',
                       'application', 'survey',
                       'modules', 'modules', 'log']

        sent_value = [i for i in sent.values()]

        AcadSummary = summarized_aspect(acad_filter, sent_value, aspect)
        ItoSummary = summarized_aspect(ito_filter, sent_value, aspect)
        ItblSummary = summarized_aspect(itbl_filter, sent_value, aspect)

        Acaddept = [i['Dept_aspect'] for i in AcadSummary]
        Itodept = [i['Dept_aspect'] for i in ItoSummary]
        Itbldept = [i['Dept_aspect'] for i in ItblSummary]

        Acadcomment = ''
        for i in Acaddept:
            Acadcomment += " ".join(i) + " "

        Itocomment = ''
        for i in Itodept:
            Itocomment += " ".join(i) + " "

        Itblcomment = ''
        for i in Itbldept:
            Itblcomment += " ".join(i) + " "

        acadWordCloud = generateWordcloud(Acadcomment)
        ItboWordCloud = generateWordcloud(Itocomment)
        ItblWordCloud = generateWordcloud(Itblcomment)

        userIsAcad = request.session['userIsAcad']
        userIsItbl = request.session['userIsItbl']
        userIsIto = request.session['userIsIto']

        contextAsp = {

            'AcadSummary': AcadSummary,
            'ItoSummary': ItoSummary,
            'ItblSummary': ItblSummary,

            'userIsAcad': userIsAcad,
            'userIsItbl': userIsItbl,
            'userIsIto': userIsIto,

            'acadWordCloud': acadWordCloud,
            'ItboWordCloud': ItboWordCloud,
            'ItblWordCloud': ItblWordCloud,

        }
        return contextAsp

    #likert
    def summaryLikert():
        _likert, dataframe, _dict = countLikert()

        contextLik = {
            'dataframe': dataframe,
            '_dict': _dict

        }
        return contextLik

    #sentiment
    def summarySentiment():

        thisSent, comp = calculateSentiment()

        contextSen = {
            'thisSent': thisSent,
            'comp': comp
        }
        return contextSen

    currentPage = "/summary/"
    context = {
        'role': UserVariables.userRole,
        'currentPage': currentPage,
        'column_name': column_name,
    }

    context.update(summaryAspect())
    context.update(summaryLikert())
    context.update(summarySentiment())


    return render(request, 'app/summary.html', context)
