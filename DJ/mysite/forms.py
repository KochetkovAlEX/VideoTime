from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Video


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
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'uk-input uk-form-width-large',
            'placeholder': 'Пароль'}
    )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'uk-input uk-form-width-large',
                'placeholder': 'Повторите Пароль'
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": 'uk-input uk-form-width-large',
                'placeholder': 'Имя пользователя'
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('name',)

    def clean_password2(self):
        """Проверка на совпадение паролей"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def save_user(self, commit=True):
        """Функция сохранения пользователя по полученным из формы данным"""
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data['password'])

        if commit:
            new_user.save()
        return new_user


class LoginForm(forms.Form):
    """Форма логина"""

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'uk-input uk-form-width-large', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'uk-input uk-form-width-large', 'placeholder': 'Пароль'}))


class VideoForm(forms.ModelForm):
    """Форма для отправки видео"""

    class Meta:
        model = Video
        fields = ('title', 'video')

    title = forms.CharField(max_length=30,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'uk-input uk-form-width-medium',
                                    'placeholder': 'Название'
                                }
                            )
                            )
    video = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'uk-input uk-form-width-medium',
            'style': 'cursor: pointer;',
            'placeholder': 'Выберите файл'
        }))


class PostForm(forms.Form):
    """Форма для комментариев"""
    post = forms.Textarea()
