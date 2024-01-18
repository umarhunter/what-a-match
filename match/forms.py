from django import forms

from .models import Person, Integer


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name']
        labels = {'name': ''}


class IntegerInputForm(forms.ModelForm):
    class Meta:
        model = Integer
        fields = ['number']