from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Username:')
        self.fields['email'].label = _('Email:')
        self.fields['password1'].label = _('Password:')
        self.fields['password2'].label = _('Confirm password:')
        
        # Help text
        self.fields['username'].help_text = _('Username must be between 6 and 20 characters.')
        self.fields['password1'].help_text = _('Password must be between 6 and 20 characters.')
        
        # Error messages
        self.fields['username'].error_messages = {
            'required': _('Username is required.'),
            'min_length': _('Username must be at least 6 characters.'),
            'max_length': _('Username must be at most 20 characters.'),
            'unique': _('A user with that username already exists.'),
        }
        self.fields['password1'].error_messages = {
            'required': _('Password is required.'),
            'min_length': _('Password must be at least 6 characters.'),
            'max_length': _('Password must be at most 20 characters.'),
        }
        self.fields['password2'].error_messages = {
            'required': _('Password confirmation is required.'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(_('Username is required.'))
        if len(username) < 6:
            raise forms.ValidationError(_('Username must be at least 6 characters.'))
        if len(username) > 20:
            raise forms.ValidationError(_('Username must be at most 20 characters.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with that email already exists.'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('The two password fields didn\'t match.'))

        print('Form data after super().clean():', cleaned_data)
        print('Form errors after super().clean():', self.errors)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.set_password is already handled by UserCreationForm
        if commit:
            user.save()
        return user
