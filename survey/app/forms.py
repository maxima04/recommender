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
 
    title = forms.ChoiceField(choices = COLUMN_CHOICES)

questions = Surveyquestions.objects.all()

ANSWER_LISTS = (('Strongly Agree', 'Strongly Agree'),
                ('Agree', 'Agree'),
                ('Disagree', 'Disagree'),
                ('Strongly Disagree', 'Strongly Disagree'))

course_list = Course.objects.values_list('id','course_name', named=True)
COURSES = [tuple([x.course_name, x.course_name]) for x in course_list]


class LikertForm(forms.Form):
    course_name = forms.CharField(max_length=70, widget=forms.Select(choices=COURSES, attrs={'class' : 'form-control'}))
    a1 = forms.CharField(label=questions[0].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a2 = forms.CharField(label=questions[1].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a3 = forms.CharField(label=questions[2].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a4 = forms.CharField(label=questions[3].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a5 = forms.CharField(label=questions[4].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a6 = forms.CharField(label=questions[5].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a7 = forms.CharField(label=questions[6].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a8 = forms.CharField(label=questions[7].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a9 = forms.CharField(label=questions[8].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a10 = forms.CharField(label=questions[9].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a11 = forms.CharField(label=questions[10].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a12 = forms.CharField(label=questions[11].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a13 = forms.CharField(label=questions[12].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a14 = forms.CharField(label=questions[13].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))

    i1 = forms.CharField(label=questions[14].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    i2 = forms.CharField(label=questions[15].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    i3 = forms.CharField(label=questions[16].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
   
    ac1 = forms.CharField(label=questions[17].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac2 = forms.CharField(label=questions[18].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac3 = forms.CharField(label=questions[19].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac4 = forms.CharField(label=questions[20].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))

class SurveyForm(forms.Form):
    course_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a4 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a5 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a6 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a7 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a8 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a9 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a10 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a11 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a12 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a13 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    a14 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    i1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    i2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    i3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
    ac1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    ac2 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    ac3 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    ac4 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class OpinionForm(forms.Form):
    e1 = forms.CharField(label=questions[21].question_description, max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    e2 = forms.CharField(label=questions[22].question_description, max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    e3 = forms.CharField(label=questions[23].question_description, max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=55, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))