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

    def clean(self):
        cd = self.cleaned_data
        number = cd.get('number')
        if number % 2 != 0:
            raise forms.ValidationError("Number must be an even number.")
