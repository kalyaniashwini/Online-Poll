from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', max_length=50, min_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match')
        username = cleaned.get('username')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'Username already exists')
        email = cleaned.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already used')
        return cleaned
