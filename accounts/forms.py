# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile  # Profile 모델 임포트

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='이름')
    last_name = forms.CharField(max_length=30, required=True, label='성')
    nickname = forms.CharField(max_length=30, required=True, label='닉네임')
    phone_number = forms.CharField(max_length=15, required=True, label='전화번호')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
            profile.nickname = self.cleaned_data['nickname']
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
        
        return user

