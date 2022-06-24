"""Модуль форм"""
from cProfile import label
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q

from . import models


class RegisterUserForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    :attrs:
    username: поле имени пользвателя
    email: поле почты пользователя
    password1: поле пароля
    password2: поле пароля
    :subclasses:
    Meta:
        :attrs:
        model: модель БД для основы формы
        fields: поля БД для сохранения 
    """
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Вася Пупкин'
                }
            )
        )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'vasya_pupkin@the_best.com'
                }
            )
        )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control shadow-sm',
                'placeholder': '**********'
                }
            )
        )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control shadow-sm',
                'placeholder': '**********'
                }
            )
        )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """
    Форма для входа пользователя
    :attrs:
    username: Логин пользователя
    password: Пароль пользователя
    """
    username = forms.CharField(
        label='Имя пользователя', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control shadow-sm rounded',
                'placeholder': 'User'
                }
            )
        )
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control shadow-sm rounded',
                'placeholder': '**********'
                }
            )
        )


class CreateResearchForm(forms.ModelForm):
    """ 
    Форма для создания исследования
    :attrs:
    research_name: поле названия исследования
    research_customer: поле наименования заказчика
    research_pattern: поле названия шаблона
    ask_published: чекбокс для публикации
    :subclasses:
    Meta:
        :attrs:
        model: модель БД для основы формы
        fields: поля БД для сохранения 
    """
    research_name = forms.CharField(
        label='Название исследования',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    research_customer = forms.ModelChoiceField(
        label='Заказчик',
        queryset=models.Customer.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    research_description = forms.CharField(
        label='Краткое описание', 
        widget = forms.Textarea(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    research_pattern = forms.ChoiceField(
        label='Шаблон',
        choices=models.Research.PATTERNS,
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    ask_published = forms.BooleanField(
        required=False, label='Опубликовать',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input me-2'
                }
            )
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research_customer'].empty_label = 'Выберите заказчика:'
    
    class Meta:
        model = models.Research
        fields = ('research_name', 'research_customer', 'research_description', 'research_pattern')
        
        
class CreateImageResearchForm(forms.ModelForm):
    """ 
    Форма для создания исследования с шабломонм Изображение
    :attrs:
    base_research: базовое исследование
    image_to_react: фото для исследования
    :subclasses:
    Meta:
        :attrs:
        model: Модель БД для основы формы
        fields: Поля БД для сохранения
    """
    base_research = forms.ModelChoiceField(
        label='Исследование',
        queryset=models.Research.objects.filter(Q(research_pattern='image')),
            widget=forms.Select(
                attrs={
                    'class': 'form-select shadow-sm rounded'
                    }
            )
        )
    image_to_react = forms.ImageField(
        label='Изображение',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_research'].empty_label = 'Выберите исследование:'
    
    class Meta:
        model = models.ImageResearch
        fields = ['base_research', 'image_to_react']
        
        
class CreateVideoResearchForm(forms.ModelForm):
    """ 
    Форма для создания исследования с шабломоном Видео
    :attrs:
    base_research: базовое исследование
    video_to_react: видео для исследования
    :subclasses:
    Meta:
        :attrs:
        model: Модель БД для основы формы
        fields: Поля БД для сохранения
    """
    base_research = forms.ModelChoiceField(
        label='Исследование',
        queryset=models.Research.objects.filter(Q(research_pattern='video')),
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    video_to_react = forms.FileField(
        label='Видеоролик',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_research'].empty_label = 'Выберите исследование:'
    
    class Meta:
        model = models.VideoResearch
        fields = ['base_research', 'video_to_react']


class EditImageResearchForm(forms.ModelForm):
    """ 
    Форма для редактирования исследования с шаблоном Изображение
    :attrs:
    image_to_react: фото для исследования
    ask_published: чекбокс для публикации
    :subclasses:
    Meta:
        :attrs:
        model: модель БД для основы формы
        fields: поля БД для сохранения 
    """
    image_to_react = forms.FileField(
        label='Изображение',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    research_description = forms.CharField(
        required=False,
        label='Краткое описание', 
        widget = forms.Textarea(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    ask_published = forms.BooleanField(
        required=False,
        label='Опубликовать',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input me-2'
                }
            )
        )
    
    class Meta:
        model = models.ImageResearch
        fields = ('image_to_react',)



class EditVideoResearchForm(forms.ModelForm):
    """ 
    Форма для редактирования исследования с шаблоном Видео
    :attrs:
    video_to_react: видео для исследования
    ask_published: чекбокс для публикации
    :subclasses:
    Meta:
        :attrs:
        model: модель БД для основы формы
        fields: поля БД для сохранения 
    """
    video_to_react = forms.FileField(
        label='Видеоролик',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    research_description = forms.CharField(
        required=False,
        label='Краткое описание', 
        widget = forms.Textarea(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    ask_published = forms.BooleanField(
        required=False,
        label='Опубликовать',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input me-2'
                }
            )
        )
    
    class Meta:
        model = models.VideoResearch
        fields = ('video_to_react',)