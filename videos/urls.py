from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<str:video_id>/', views.video_detail, name='video_detail'),
    path('upload/', views.upload_video, name='upload_video'),
    path('api/like/<str:video_id>/', views.like_video, name='like_video'),
    path('api/comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("", views.home, name="home"),
]
