from django import forms
from django.forms import BaseFormSet

from .models import Integer

class InputForm(forms.Form):
    name = forms.CharField(max_length=20)


class IntegerInputForm(forms.ModelForm):
    class Meta:
        model = Integer
        fields = ['number']

    def clean(self):
        cd = self.cleaned_data
        number = cd.get('number')
        if number % 2 != 0:
            raise forms.ValidationError("Number must be an even number.")
