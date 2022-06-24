"""
Модуль для добавления url-адресов страниц
"""
from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path('', views.ShowMainPage.as_view(), name='main'),
    path('researches', views.ShowAvailiableResearchesView.as_view(), name='researches'),
    path('answer_image/<int:pk>/', views.AnswerImageResearchView.as_view() ,name='answer_image'),
    path('answer_video/<int:pk>/', views.AnswerVideoResearchView.as_view() ,name='answer_video'),
]

