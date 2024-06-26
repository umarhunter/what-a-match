from django import forms
from django.forms import BaseFormSet

from .models import Integer


class InputForm(forms.Form):
    name = forms.CharField(max_length=20)

    def clean(self):
        cd = self.cleaned_data
        name = cd.get('name')
        if len(name) <= 1:
            raise forms.ValidationError("Name must be longer than 1 letter")



class PrefsInputForm(forms.Form):
    preferences = forms.CharField()

    def clean(self):
        cd = self.cleaned_data
        names = cd.get('preferences')
        if len(names) <= 1:
            raise forms.ValidationError("Name must be longer than 1 letter")


class IntegerInputForm(forms.ModelForm):
    class Meta:
        model = Integer
        fields = ['number']

    def clean(self):
        cd = self.cleaned_data
        number = cd.get('number')
        if number % 2 != 0:
            raise forms.ValidationError("Number must be an even number.")
        elif number <= 2:
            raise forms.ValidationError("Number cannot be <= 2.")
        elif number > 10:
            raise forms.ValidationError("As this is just a demo, please use a sample of <= 10")