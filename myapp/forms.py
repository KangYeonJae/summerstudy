from django import forms
from .models import Myapp

class MyappForm(forms.ModelForm):
    class Meta:
        model=Myapp
        fields=['title', 'body']