from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=6, max_length=20)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not (6 <= len(username) <= 20):
            raise ValidationError("Nazwa użytkownika musi mieć od 6 do 20 znaków.")
        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Hasła nie są zgodne")

        if password and not (6 <= len(password) <= 20):
            self.add_error('password', "Hasło musi mieć od 6 do 20 znaków.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Od 6 do 20 znaków." # Updated help text
        self.fields['password'].help_text = None
        self.fields['password2'].help_text = None # No help text for password confirmation

    def clean(self):
        cleaned_data = super().clean()
        print('Form data after super().clean():', cleaned_data)
        print('Form errors after super().clean():', self.errors)
        return cleaned_data

    # Removed debugging clean method temporarily
    # def clean(self):
    #     cleaned_data = super().clean()
    #     print('Form data:', cleaned_data)
    #     print('Password:', cleaned_data.get('password'))
    #     print('Password2:', cleaned_data.get('password2'))
    #     return cleaned_data 