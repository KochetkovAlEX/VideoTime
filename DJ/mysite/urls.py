from django.urls import path

from . import views

app_name = "VideoTime"

urlpatterns = [
    path('', views.test_render, name='main_page'),
    # path('', views.load_next_video, name='header_page'),
    # path('<int:id>/', views.main_page, name='index'),
    path('reg/', views.reg_page, name='reg_page'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload_video/', views.upload_video, name='upload'),
    path("profile/<int:user_id>", views.load_user_page, name='userpage'),
    path('video-delete/<int:video_id>', views.delete_video, name='delete_video')
    # path('likes/<int:id>', views.get_like, name='like'),
    # path('next_video/<int:id>', views.main_page, name='next_video')
]
