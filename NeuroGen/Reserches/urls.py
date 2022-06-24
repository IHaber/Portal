"""
Модуль для добавления url-адресов страни
"""
from django.urls import path
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path('', views.ShowPortalPage.as_view(), name='index'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('develop', views.ShowDevelopView.as_view(), name = 'develop'),
    path('published', views.ShowPublishView.as_view(), name = 'published'),
    path('logout', views.logout_user, name='logout'),
    path('create_research', views.CreateResearchView.as_view(), name='create_research'),
    path('delete_research/<int:pk>', views.delete_research, name='delete_research'),
    path('finish_research/<int:pk>', views.finish_research, name='finish_research'),
    path('image_creation', views.CreateImageResearchView.as_view(), name='image_creation'),
    path('video_creation', views.CreateVideoResearchView.as_view(), name='video_creation'),
    path('edit_image/<int:pk>/', views.EditImageResearchView.as_view(), name='edit_image'),
    path('edit_video/<int:pk>/', views.EditVideoResearchView.as_view(), name='edit_video'),
    path('view_image/<int:pk>/', views.DetailImageView.as_view(), name='view_image'),
    path('view_video/<int:pk>/', views.DetailVideoView.as_view(), name='view_video'),
    path('image_export/<int:pk>/', views.export_image_xls, name='image_export'), 
    path('video_export/<int:pk>/', views.export_video_xls, name='video_export'),
    
]
