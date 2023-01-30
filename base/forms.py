from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Post,Tag
from django.forms import ModelForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','image','email']

class UserForm2(ModelForm):

    class Meta:
        model=User
        fields=['username','image','email','password']

class PostForm(ModelForm):
    class Meta:
        model=Post        
        fields=['name','image','caption']

class UpdateForm(ModelForm):
    class Meta:
        model=User
        fields='__all__'        

class TagForm(forms.Form):
    name=forms.CharField()