from django.shortcuts import render
from .forms import UserRegistrationForm, LoginForm, VideoForm, PostForm
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser
from .service import *
from .template_name import *


class SignUpView(generic.CreateView):
    """Класс, требующийся для регистарции пользователя"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = reg_page_template


def main_page(request, id):
    """Веб-сервис, загружающий главную страницу"""
    context = check_post_database(request, id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post(post=request.POST.get('comment_place'), user=request.user, video=context['video']).save()
            return render(request, main_page_template, context=context)
    return render(request, main_page_template, context=context)


def load_next_video(request):  # request нужен в данной функции, но Pycharm красит его в серый.
    """Выбирает случайное следующее видео"""
    video = Video.objects.all()
    next_video_id = random.choice(video).id
    return redirect(f'/{next_video_id}')


def reg_page(request):
    """Сервис для регистарции пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = save_user(user_form).save()
            return render(request, reg_page_done_template, {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, reg_page_template, {'user_form': user_form})


def user_login(request):
    """Веб-сервис для ауентификации пользователя"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            after_login_actions = authenticate_and_login_user(form, request)
            return after_login_actions
    else:
        form = LoginForm()
    return render(request, login_page_template, {'form': form})


def upload_video(request):
    """Веб-сервис загрузки видео на сайт"""
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            Video(title=form.cleaned_data['title'], video=form.cleaned_data['video'], user=request.user).save()
            return redirect('first')
    else:
        form = VideoForm()
    return render(request, upload_video_template, {'form': form})


def load_user_page(request, user_id: int):
    """Веб-сервис для загрузки странциы пользователя по его id - user_id;
        собиарет количество лайков на видео пользователя"""
    user = CustomUser.objects.get(id=user_id)
    video = Video.objects.filter(user=user_id)
    like = []
    for i in video:
        like.append(list(i.likes.values()).count(True))
    return render(request, user_page_template, {"user": user, "video": video, "like": like})


def get_like(request, id: int):
    """Функция, позволяющая ставить лайки на определенное видео по его id"""
    current_video = Video.objects.get(id=id)
    user_like_status(request, current_video).save()
    return redirect(f'/{id}')
