from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Note_create_form(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'description']


class Homework_create_form(forms.ModelForm):

    class Meta:
        model = Homework
        fields = ['subject','title', 'description']

class Dashboard_Search(forms.Form):
    text = forms.CharField(max_length=1000,label='enter your search')

class TodoCreate_form(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurements = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)

class ConvertLength(forms.Form):
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(label='',widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='',widget=forms.Select(choices=CHOICES))

class ConvertMass(forms.Form):
    CHOICES = [('pound','Pound'),('kg','Kg')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(label='',widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='',widget=forms.Select(choices=CHOICES))


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']