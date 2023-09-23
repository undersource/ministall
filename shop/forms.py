from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Confirm Password'}))
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}))
    captcha = CaptchaField()

class ChangePasswordForm(forms.ModelForm):
    oldpassword = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Old Password'}))
    newpassword1 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'New Password'}))
    newpassword2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Confirm New Password'}))

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise ValidationError("Two passwords didn't match")
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('oldpassword', 'newpassword1', 'newpassword2')

class DeleteAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}))

    class Meta:
        model = get_user_model()
        fields = ['password']