import random
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Video, Post


def get_all_data_from_database(request, id) -> dict:
    """Собирает данные из бд о текущем видео и генерирует номер следующего"""
    video = Video.objects.all().count()
    current_video = Video.objects.get(id=id)
    user_id = request.user.id
    next_id = random.randint(1, video)
    context = {
        'video': current_video,
        "user_id": user_id,
        'next_id': next_id,
        "cur_id": current_video.id
    }
    return context


def check_post_database(request, id) -> dict:
    """Функция для проверки существования комментариев к определенному видео"""
    context = get_all_data_from_database(request, id)
    if Post.objects.filter(video=context['video']) is not None:
        context['postform'] = Post.objects.filter(video=context['video'])
        return context
    return context


def user_like_status(request, video) -> object:
    """Проверяет на наличие пользовательского id в списке лайкнувших видео и
    проверяет, какую реакцию на видео он оставил"""
    if str(request.user.id) in video.likes.keys():
        if video.likes[f'{request.user.id}'] is True:
            video.likes[f'{request.user.id}'] = False
        else:
            video.likes[f'{request.user.id}'] = True
    else:
        video.likes[f'{request.user.id}'] = True
    return video


def save_user(user_form):
    """Функция сохранения пользователя по полученным из формы данным"""
    new_user = user_form.save(commit=False)
    new_user.set_password(user_form.cleaned_data['password'])
    return new_user


def authenticate_and_login_user(form, request):
    """Функция для ауентификации и авторизации пользователя.
    принимает в себя форму, содержащую данные нового пользователя"""
    cd = form.cleaned_data
    user = authenticate(username=cd['username'], password=cd['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            user_login_successful = redirect('first')
            return user_login_successful
    else:
        invalid_login = HttpResponse('Invalid login')
        return invalid_login
