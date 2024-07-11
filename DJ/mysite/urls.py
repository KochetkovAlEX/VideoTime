from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.load_next_video, name='first'),
    path('<int:id>/', views.main_page, name='index'),
    path('reg/', views.reg_page, name='reg_page'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html', next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('upload_video/', views.upload_video, name='upload'),
    path("profile/<int:user_id>", views.load_user_page, name='userpage'),
    path('likes/<int:id>', views.get_like, name='like'),
    path('next_video/<int:id>', views.main_page, name='next_video')
]