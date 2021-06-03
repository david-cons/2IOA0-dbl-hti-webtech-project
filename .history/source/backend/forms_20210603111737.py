from django import forms

class timeForm(forms.Form):
    startDate = forms.CharField(max_length=100)
    endDate =  forms.CharField(max_length=100)