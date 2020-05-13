from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice


class DateInput(forms.DateInput):
    input_type = 'date'




class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text','pub_date']
        widgets ={
            'pub_date': DateInput(),
        }

class ChoiceCreateForm(forms.ModelForm):
    
    class Meta:
        model = Choice
        fields = ['choice_text','choice_text']


