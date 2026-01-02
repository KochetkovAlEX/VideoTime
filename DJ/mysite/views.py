from django.shortcuts import render, get_object_or_404
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

def test_render(request):
    return render(request, base_page)


def reg_page(request):
    """Функция для регистарции пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = save_user(user_form)
            login(request, new_user)
            return render(request, base_page, {'user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, reg_page_template, {'user_form': user_form})


def user_login(request):
    """Функция для ауентификации пользователя"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            after_login_actions = authenticate_and_login_user(form, request)
            return after_login_actions
    else:
        form = LoginForm()
    return render(request, login_page_template, {'form': form})


def upload_video(request):
    """Функция загрузки видео на сайт"""
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_url = upload_video_to_cloud(form)
            Video(title=form.cleaned_data['title'], video_url=video_url, user=request.user).save()
            return redirect('VideoTime:upload')
    else:
        form = VideoForm()
    return render(request, upload_video_template, {'form': form})


def load_user_page(request, user_id: int):
    """
    Функция для загрузки странциы пользователя по его id - user_id;
    собиарет количество лайков на видео пользователя
    """
    user = CustomUser.objects.get(id=user_id)
    video = Video.objects.filter(user=user_id)
    like = []
    for i in video:
        like.append(list(i.likes.values()).count(True))
    return render(request, user_page_template, {"user": user, "video": video, "like": like})

def delete_video(request, video_id: int):
    """Функция для удаления видео по его id"""
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('VideoTime:userpage', user_id=request.user.id)


# def main_page(request, id):
#     """Функция, загружающая главную страницу"""
#     context = check_post_database(request, id)
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             Post(post=request.POST.get('comment_place'), user=request.user, video=context['video']).save()
#             return render(request, main_page_template, context=context)
#     return render(request, main_page_template, context=context)


# def load_next_video(request):  # request нужен в данной функции, но Pycharm красит его в серый.
#     """Выбирает случайное следующее видео"""
#     video = Video.objects.all()
#     next_video_id = random.choice(video).id
#     return redirect(f'/{next_video_id}')


# def get_like(request, id: int):
#     """Функция, позволяющая ставить лайки на определенное видео по его id"""
#     current_video = Video.objects.get(id=id)
#     user_like_status(request, current_video).save()
#     # return redirect(f'/{id}')




