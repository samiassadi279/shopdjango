from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

class SignUp(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username","email", "password1","password2")

    def save(self, commit=True):
        user = super(SignUp, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_username(self):
        email=self.cleaned_data.get("email")
        username=self.cleaned_data.get("username")
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.error_messages['username_exists']="username already exists"
            raise forms.ValidationError(
            self.error_messages['username_exists'],
                code='username_exists',
            )
        return username