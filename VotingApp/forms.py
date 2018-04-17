from django import forms

from .validators import validate_fl_name


class RegistrationForm(forms.Form):
    fl_name = forms.CharField(validators=[validate_fl_name])
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
