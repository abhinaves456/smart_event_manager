from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# A form for new users to sign up
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')