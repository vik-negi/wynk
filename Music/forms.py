import email
from django import forms


class subscriberForm(forms.Form):
    firstname = forms.CharField(label="First Name", max_length=50)
    lastname = forms.CharField(label="Last Name", max_length=100)
    age = forms.IntegerField()
    gender = forms.IntegerField()
    email = forms.EmailField(max_length=50)
    moblieno = forms.IntegerField()
    