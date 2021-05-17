from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from app.forms import SurveyForm, LikertForm, OpinionForm, RegistrationForm, LoginForm, TitleForm
from .models import Surveyquestions, User, Likert, Opinion, Survey
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

def login_user(username, password):
    if User.objects.filter(username=username, password=password):
        userIsUser = 0
        userIsAdmin = 0
        userIsItbl = 0
        userIsIto = 0
        userIsAcads = 0

        getUser = User.objects.filter(username=username, password=password)
        for userInfo in getUser:
            UserVariables.userId = userInfo.id
            UserVariables.userName = userInfo.username
            userIsUser = userInfo.is_user
            userIsAdmin = userInfo.is_admin
            userIsItbl = userInfo.is_itbl
            userIsIto = userInfo.is_ito
            userIsAcads = userInfo.is_acads

        if userIsUser == 1:
            UserVariables.userRole = "student"
            page = "/survey"
        elif userIsAdmin == 1:
            UserVariables.userRole = "admin"
            page = "/dashboard"
        elif userIsItbl == 1:
            UserVariables.userRole = "itbl"
            page = "/aspectChart"
        elif userIsIto == 1:
            UserVariables.userRole = "acads"
            page = "/aspectChart"
        elif userIsAcads == 1:
            UserVariables.userRole = "ito"
            page = "/aspectChart"
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
        messages.error(request, "You need to login!")
        return redirect('/login')


    if request.method == 'POST':

        surveyform = SurveyForm(request.POST)
        likertForm = LikertForm(request.POST)
        opinionForm = OpinionForm(request.POST)

        if surveyform.is_valid() and likertForm.is_valid() and opinionForm.is_valid():
            '''
            !!! Note !!!
            Try to print a1 variable if form.cleaned_data.get() is working accordingly
            you can remove controller.py if it takes too long to load
            '''
            
            #Get likert form data
            #a1 = likertForm.cleaned_data.get('a1')
            #a2 = likertForm.cleaned_data.get('a2')
            #Please contiue until finished

            # Likert data
            courseName = likertForm.cleaned_data['course_name']
            a1 = likertForm.cleaned_data['a1']
            a2 = likertForm.cleaned_data['a2']
            a3 = likertForm.cleaned_data['a3']
            a4 = likertForm.cleaned_data['a4']
            a5 = likertForm.cleaned_data['a5']
            a6 = likertForm.cleaned_data['a6']
            a7 = likertForm.cleaned_data['a7']
            a8 = likertForm.cleaned_data['a8']
            a9 = likertForm.cleaned_data['a9']
            a10 = likertForm.cleaned_data['a10']
            a11 = likertForm.cleaned_data['a11']
            a12 = likertForm.cleaned_data['a12']
            a13 = likertForm.cleaned_data['a13']
            a14 = likertForm.cleaned_data['a14']
            a15 = likertForm.cleaned_data['a15']
            a16 = likertForm.cleaned_data['a16']
            a17 = likertForm.cleaned_data['a17']
            a18 = likertForm.cleaned_data['a18']
            i1 = likertForm.cleaned_data['i1']
            i2 = likertForm.cleaned_data['i2']
            i3 = likertForm.cleaned_data['i3']
            ac1 = likertForm.cleaned_data['ac1']
            ac2 = likertForm.cleaned_data['ac3']
            ac3 = likertForm.cleaned_data['ac3']
            ac4 = likertForm.cleaned_data['ac4']
            ac5 = likertForm.cleaned_data['ac5']
            ac6 = likertForm.cleaned_data['ac6']
            ac7 = likertForm.cleaned_data['ac7']
            ac8 = likertForm.cleaned_data['ac8']

            likert_data = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,i1,i2,i3,ac1,ac2,ac3,ac4,ac5,ac6,ac7,ac8]
            #uploadDataLikert(likert_data) ## upload form data to csv

            #Get opinion form data, do not include subject name
            sa1 = surveyform.cleaned_data['a1']
            sa2 = surveyform.cleaned_data['a2']
            sa3 = surveyform.cleaned_data['a3']
            sa4 = surveyform.cleaned_data['a4']
            sa5 = surveyform.cleaned_data['a5']
            sa6 = surveyform.cleaned_data['a6']
            sa7 = surveyform.cleaned_data['a7']
            sa8 = surveyform.cleaned_data['a8']
            sa9 = surveyform.cleaned_data['a9']
            sa10 = surveyform.cleaned_data['a10']
            sa11 = surveyform.cleaned_data['a11']
            sa12 = surveyform.cleaned_data['a12']
            sa13 = surveyform.cleaned_data['a13']
            sa14 = surveyform.cleaned_data['a14']
            sa15 = surveyform.cleaned_data['a15']
            sa16 = surveyform.cleaned_data['a16']
            sa17 = surveyform.cleaned_data['a17']
            sa18 = surveyform.cleaned_data['a18']
            si1 = surveyform.cleaned_data['i1']
            si2 = surveyform.cleaned_data['i2']
            si3 = surveyform.cleaned_data['i3']
            sac1 = surveyform.cleaned_data['ac1']
            sac2 = surveyform.cleaned_data['ac3']
            sac3 = surveyform.cleaned_data['ac3']
            sac4 = surveyform.cleaned_data['ac4']
            sac5 = surveyform.cleaned_data['ac5']
            sac6 = surveyform.cleaned_data['ac6']
            sac7 = surveyform.cleaned_data['ac7']
            sac8 = surveyform.cleaned_data['ac8']

            survey_data = [sa1,sa2,sa3,sa4,sa5,sa6,sa7,sa8,sa9,sa10,sa11,sa12,sa13,sa14,sa15,sa16,sa17,sa18,si1,si2,si3,sac1,sac2,sac3,sac4,sac5,sac6,sac7,sac8]
            #uploadDataSentiment(survey_data) ## upload form data to csv

            #Get opinion form data
            e1 = opinionForm.cleaned_data['e1']
            e2 = opinionForm.cleaned_data['e2']
            e3 = opinionForm.cleaned_data['e3']

            ### No function for here yet
            opinion_data = [e1,e2,e3]

            timeStamp = timezone.make_naive(timezone.now())
            user_id=UserVariables.userId

            #save data to database
            likertData = Likert(user_id=user_id, course_name=courseName, timestamp=timeStamp, a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12, a13=a13, a14=a14, a15=a15, a16=a16, a17=a17, a18=a18, i1=i1, i2=i2, i3=i3, ac1=ac1, ac2=ac2, ac3=ac3, ac4=ac4, ac5=ac5, ac6=ac6, ac7=ac7, ac8=ac8)
            likertData.save()

            surveyData = Survey(user_id=user_id, course_name=courseName, timestamp=timeStamp, a1=sa1, a2=sa2, a3=sa3, a4=sa4, a5=sa5, a6=sa6, a7=sa7, a8=sa8, a9=sa9, a10=sa10, a11=sa11, a12=sa12, a13=sa13, a14=sa14, a15=sa15, a16=sa16, a17=sa17, a18=sa18, i1=si1, i2=si2, i3=si3, ac1=sac1, ac2=sac2, ac3=sac3, ac4=sac4, ac5=sac5, ac6=sac6, ac7=sac7, ac8=sac8)
            surveyData.save()

            opinionData = Opinion(user_id=user_id, e1=e2, e2=e2, e3=e3)
            opinionData.save()

            messages.success(request, "Submitted successfully!")
            return render(request, 'app/survey.html')
            
    # if a GET (or any other method) we'll create a blank form
    else:
        surveyform = SurveyForm()
        likertform = LikertForm()
        opinionform = OpinionForm()

        questions = Surveyquestions.objects.all()

        zipped_data = zip(likertform, surveyform)
        survey = list(zipped_data)
        currentPage = "/survey/"
        context = {
            'form': survey,
            'questions': questions,
            'opinionform': opinionform,
            'currentPage': currentPage,
        }

        return render(request, 'app/survey.html', context)

def about(request):
    return render(request, 'app/about.html')


def likertPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        messages.error(request, "You need to login!")
        return redirect('/login')


    likert = countLikert()
    likert = json.dumps(likert)
    currentPage = "/likertChart/"

    context = {
        'column_name':column_name,
        'likert':likert,
        'currentPage': currentPage
        }

    return render(request, 'app/likertChart.html', context)

def sentimentPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        messages.error(request, "You need to login!")
        return redirect('/login')

    sentiment = calculateSentiment()
    currentPage = "/sentimentChart/"
    context = {
        'sentiment':sentiment,
        'column_name':column_name,
        'currentPage': currentPage
        }

    return render(request, 'app/sentimentChart.html', context)

def aspectPage(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        messages.error(request, "You need to login!")
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
    currentPage = "/aspectChart/"

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
        'currentPage': currentPage,

        
    }


    return render(request, 'app/aspectChart.html', context)

def login(request):

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            userpass = loginForm.cleaned_data['password']

            redirectToPage = login_user(username, userpass)

            if redirectToPage != "/login":
                message = "Hello " + UserVariables.userName + "!"
                messages.success(request, message)
            else:
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

            message = "Hello " + UserVariables.userName + "!"
            messages.success(request, message)

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

def submitted(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        messages.error(request, "You need to login!")
        return redirect('/login')

    message = "Submitted Successfully!"
    context = {
        'message': message,
    }

    return render(request, 'app/thankyou.html', context)

def dashboard(request):
    # check if user logged in if not, redirect to login page
    redirectUser = user_auth()
    if redirectUser == True:
        messages.error(request, "You need to login!")
        return redirect('/login')

    context = {

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