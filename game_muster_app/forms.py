from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(forms.ModelForm):

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENRES_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    username = forms.CharField(widget=forms.TextInput, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    first_name = forms.CharField(widget=forms.TextInput, required=True)
    last_name = forms.CharField(widget=forms.TextInput, required=True)
    birthday = forms.DateField(widget=forms.DateInput, required=True)
    gender = forms.ChoiceField(choices=GENRES_CHOICES, required=True)
    avatar_image: forms.ImageField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label or 'Enter username here...'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'Enter email here...'
        self.fields['first_name'].widget.attrs['placeholder'] = self.fields['first_name'].label or 'Enter first name here...'
        self.fields['last_name'].widget.attrs['placeholder'] = self.fields['last_name'].label or 'Enter last name here...'
        self.fields['birthday'].widget.attrs['placeholder'] = self.fields['birthday'].label or 'Year-month-day...'
        self.fields['gender'].label = 'Gender'
        self.fields['avatar_image'].label = 'User Avatar'
        self.fields['password'].widget.attrs['placeholder'] = self.fields['password'].label or 'Enter password here...'
        self.fields['confirm_password'].widget.attrs['placeholder'] = self.fields['confirm_password'].label or 'Confirm password...'

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net', 'xyz']:
            raise forms.ValidationError(f'Registration for domain {domain} impossible.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This name {username} is taken. Try something else.')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'birthday',
            'avatar_image',
            'gender',
            'password',
            'confirm_password'
        ]


class LoginForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label or 'Enter username here...'
        self.fields['password'].widget.attrs['placeholder'] = self.fields['password'].label or 'Enter password here...'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f'User with login {username} was not found in the system!')
        if not user.check_password(password):
            raise forms.ValidationError('Invalid password')
        return self.cleaned_data


class CustomChangeForm(PasswordChangeForm):

    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(label='Enter new password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password here...'}), required=True)
    new_password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat new password here...'}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = self.fields['old_password'].label or 'Enter old password here...'

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class UpdateProfileForm(forms.ModelForm):

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENRES_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    username = forms.CharField(widget=forms.TextInput, required=True)
    first_name = forms.CharField(widget=forms.TextInput, required=True)
    last_name = forms.CharField(widget=forms.TextInput, required=True)
    birthday = forms.DateField(widget=forms.DateInput, required=True)
    gender = forms.ChoiceField(choices=GENRES_CHOICES, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'birthday',
            'gender',
        ]
