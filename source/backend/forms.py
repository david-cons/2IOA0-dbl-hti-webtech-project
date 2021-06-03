from django import forms

class timeForm(forms.Form):
    startDate = forms.CharField(label = "start_date", max_length=100)
    endDate =  forms.CharField(label = "end_date", max_length=100)