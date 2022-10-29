from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm 
from .models import User


class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'avatar', 'email', 'bio']
        labels = {
            'name': 'Full Name'
        }

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'bio', 'password1', 'password2']
        



