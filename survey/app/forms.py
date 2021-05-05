from django import forms
from .models import Surveyquestions

questions = Surveyquestions.objects.all()

ANSWER_LISTS = (('Strongly Agree', 'Strongly Agree'),
                ('Agree', 'Agree'),
                ('Disagree', 'Disagree'),
                ('Strongly Disagree', 'Strongly Disagree'),
                ('N/A', 'N/A'))


class LikertForm(forms.Form):
    course_name = forms.CharField(max_length=70)
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
    
    a15 = forms.CharField(label=questions[15].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a16 = forms.CharField(label=questions[16].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a17 = forms.CharField(label=questions[17].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    a18 = forms.CharField(label=questions[18].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))

    i1 = forms.CharField(label=questions[19].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    i2 = forms.CharField(label=questions[20].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    i3 = forms.CharField(label=questions[21].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
   
    ac1 = forms.CharField(label=questions[23].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac2 = forms.CharField(label=questions[24].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac3 = forms.CharField(label=questions[25].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    
    ac4 = forms.CharField(label=questions[26].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac5 = forms.CharField(label=questions[28].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac6 = forms.CharField(label=questions[29].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac7 = forms.CharField(label=questions[30].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))
    ac8 = forms.CharField(label=questions[31].question_description, max_length=255, widget=forms.RadioSelect(choices=ANSWER_LISTS))

class SurveyForm(forms.Form):
    course_name = forms.CharField(max_length=70)
    a1 = forms.CharField(max_length=255)
    a2 = forms.CharField(max_length=255)
    a3 = forms.CharField(max_length=255)
    a4 = forms.CharField(max_length=255)
    a5 = forms.CharField(max_length=255)
    a6 = forms.CharField(max_length=255)
    a7 = forms.CharField(max_length=255)
    a8 = forms.CharField(max_length=255)
    a9 = forms.CharField(max_length=255)
    a10 = forms.CharField(max_length=255)
    a11 = forms.CharField(max_length=255)
    a12 = forms.CharField(max_length=255)
    a13 = forms.CharField(max_length=255)
    
    a14 = forms.CharField(max_length=255)
    a15 = forms.CharField(max_length=255)
    a16 = forms.CharField(max_length=255)
    a17 = forms.CharField(max_length=255)
    a18 = forms.CharField(max_length=255)
    
    i1 = forms.CharField(max_length=255)
    i2 = forms.CharField(max_length=255)
    i3 = forms.CharField(max_length=255)
    
    ac1 = forms.CharField(max_length=255)
    ac2 = forms.CharField(max_length=255)
    ac3 = forms.CharField(max_length=255)
    ac4 = forms.CharField(max_length=255)
    ac5 = forms.CharField(max_length=255)
    ac6 = forms.CharField(max_length=255)
    ac7 = forms.CharField(max_length=255)
    ac8 = forms.CharField(max_length=255)

class OpinionForm(forms.Form):
    e1 = forms.CharField(label="26. What I like best in Canvas is/are: ", max_length=255)
    e2 = forms.CharField(label="27. What I like least in Canvas is/are:  ", max_length=255)
    e3 = forms.CharField(label="28. I would like to suggest:  ", max_length=255)

class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=55)
    username = forms.CharField(label="Username", max_length=255)
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255)
    password = forms.CharField(label="Password", max_length=55, widget=forms.PasswordInput)