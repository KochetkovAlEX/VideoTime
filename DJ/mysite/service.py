import random
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Video, Post
import boto3
from .forms import VideoForm
from django.conf import settings
cloud_config = settings.YANDEX_CLOUD_CONFIG


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
    return user_form.save_user()


def authenticate_and_login_user(form, request):
    """Функция для ауентификации и авторизации пользователя.
    Принимает в себя форму, содержащую данные нового пользователя"""
    cd = form.cleaned_data
    user = authenticate(username=cd['username'], password=cd['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('VideoTime:main_page')
    else:
        return HttpResponse('Не получилось войти')


def upload_video_to_cloud(form: VideoForm):
    """Функция загрузки данных """

    vide_title = form.cleaned_data['title']

    s3_client = boto3.client(
        's3',
        endpoint_url=cloud_config['endpoint_url'],
        aws_access_key_id=cloud_config['access_key'],
        aws_secret_access_key=cloud_config['secret_key'],
        region_name=cloud_config['region']
    )


    s3_client.upload_fileobj(
        form.cleaned_data['video'],  # файловый объект, а не путь
        cloud_config['bucket_name'],  # имя bucket
        vide_title
    )

    url = f"https://{cloud_config['bucket_name']}.storage.yandexcloud.net/{vide_title}"
    return url
