import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from .forms import UserRegistrationForm, LoginForm, VideoForm, PostForm
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Video, Post
from django.contrib.auth.models import User


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "reg_page.html"


def main_page(request, id):
    video = Video.objects.all().count()
    next_video = Video.objects.get(id=id)
    user_id = request.user.id
    next_id = random.randint(1, video)
    context = {
        'video': next_video,
        "user_id": user_id,
        'next_id': next_id,
        "cur_id": next_video.id
    }
    try:
        post = Post.objects.filter(video=next_video)
        context['postform'] = post
    except:
        ...
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            Post(post=request.POST.get('comment_place'), user=request.user, video=next_video).save()
            return render(request, 'index.html', context=context)
    else:
        form = PostForm()
    return render(request, 'index.html', context=context)


def next_video(request):
    video = Video.objects.all().count()
    id = random.randint(1, video)
    return redirect(f'/{id}')


def reg_page(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'reg_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'reg_page.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('first')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            Video(title=form.cleaned_data['title'], video=form.cleaned_data['video'], user=request.user).save()
            video = Video.objects.all()
            print(video.values())
            context = {
                'form': form,
                "video": video
            }
            return redirect('first')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})


def load_userpage(request, user_id):
    user = User.objects.get(id=user_id)
    video = Video.objects.filter(user=user_id)
    like = []
    for i in video:
        like.append(list(i.likes.values()).count(True))
    return render(request, "userpage.html", {"user": user, "video": video, "like": like})


def get_like(request, id):
    video = Video.objects.get(id=id)
    if str(request.user.id) in video.likes.keys():
        if video.likes[f'{request.user.id}'] == True:
            video.likes[f'{request.user.id}'] = False
        else:
            video.likes[f'{request.user.id}'] = True
    else:
        video.likes[f'{request.user.id}'] = True
    # print(list(video.likes.values()).count(True))  # сумма всех лайков
    video.save()
    return redirect(f'/{id}')
