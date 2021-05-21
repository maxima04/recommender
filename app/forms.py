from django import forms
from .models import Surveyquestions, Course
from pathlib import Path
import os
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent.parent
COMMONS_DIR = os.path.join(BASE_DIR, 'app/commons')
OPINION_SURVEY_DIR = os.path.join(COMMONS_DIR,'opinion_survey.csv')

op_col = pd.read_csv(OPINION_SURVEY_DIR)

opinion_column = [tuple([col,col]) for col in op_col.columns]

COLUMN_CHOICES = opinion_column

class TitleForm(forms.Form):
    #title = forms.ChoiceField(choices = COLUMN_CHOICES)
    title = forms.CharField(widget=forms.Select(choices=COLUMN_CHOICES, attrs={'class': 'form-control'}))

questions = Surveyquestions.objects.all()

ANSWER_LISTS = (('Strongly Agree', 'Strongly Agree'),
                ('Agree', 'Agree'),
                ('Disagree', 'Disagree'),
                ('Strongly Disagree', 'Strongly Disagree'))

course_list = Course.objects.values_list('id','course_name', named=True)
COURSES = [tuple([x.course_name, x.course_name]) for x in course_list]

class LikertSurveyForm(forms.Form):
    course_name = forms.CharField(max_length=70, widget=forms.Select(choices=COURSES, attrs={'class' : 'form-control'}))

    #1
    a1 = forms.CharField(label=questions[0].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa1 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #2
    a2 = forms.CharField(label=questions[1].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa2 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #3
    a3 = forms.CharField(label=questions[2].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa3 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #4
    a4 = forms.CharField(label=questions[3].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa4 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #5
    a5 = forms.CharField(label=questions[4].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa5 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #6
    a6 = forms.CharField(label=questions[5].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa6 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #7
    a7 = forms.CharField(label=questions[6].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa7 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #8
    a8 = forms.CharField(label=questions[7].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa8 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #9
    a9 = forms.CharField(label=questions[8].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa9 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #10
    a10 = forms.CharField(label=questions[9].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa10 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #11
    a11 = forms.CharField(label=questions[10].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa11 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #12
    a12 = forms.CharField(label=questions[11].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa12 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #13
    a13 = forms.CharField(label=questions[12].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa13 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #14  question.13.question_description
    a14 = forms.CharField(label=questions[14].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a15 = forms.CharField(label=questions[15].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a16 = forms.CharField(label=questions[16].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a17 = forms.CharField(label=questions[17].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sa14 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    #15 - 17
    i1 = forms.CharField(label=questions[18].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    si1 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    i2 = forms.CharField(label=questions[19].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    si2 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    i3 = forms.CharField(label=questions[20].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    si3 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    #18 question.21.question_description
    ac1 = forms.CharField(label=questions[22].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac2 = forms.CharField(label=questions[23].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac3 = forms.CharField(label=questions[24].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sac1 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    #19
    ac4 = forms.CharField(label=questions[25].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sac2 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #20 question.26.question_description
    ac5 = forms.CharField(label=questions[27].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac6 = forms.CharField(label=questions[28].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac7 = forms.CharField(label=questions[29].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sac3 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #21
    ac8 = forms.CharField(label=questions[30].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    sac4 = forms.CharField(label="Comment", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    #opinion
    e1 = forms.CharField(label=questions[31].question_description, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    e2 = forms.CharField(label=questions[32].question_description, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    e3 = forms.CharField(label=questions[33].question_description, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))



class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=55, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))