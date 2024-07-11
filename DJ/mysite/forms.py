from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Video
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя"""
    class Meta:
        model = CustomUser
        fields = ('name',)


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя"""
    class Meta:
        model = CustomUser
        fields = ('name',)


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации"""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('name',)

    def clean_password2(self):
        """Проверка на совпадение паролей"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    """Форма логина"""
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class VideoForm(forms.ModelForm):
    """Форма для отправки видео"""
    class Meta:
        model = Video
        fields = ('title', 'video')

    title = forms.CharField(max_length=30)
    video = forms.FileField()


class PostForm(forms.Form):
    """Форма для комментариев"""
    post = forms.Textarea()
