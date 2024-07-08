from django.forms import modelform_factory
from django import forms
from django.contrib.auth.models import User
from .models import Video

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # photo = forms.ImageField()


class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video')

    title = forms.CharField(max_length=30)
    video = forms.FileField()


class PostForm(forms.Form):
    post = forms.Textarea()