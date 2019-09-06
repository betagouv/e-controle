from django import forms


class WelcomeForm(forms.Form):
    agree = forms.BooleanField()
