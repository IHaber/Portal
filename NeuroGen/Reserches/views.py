"""
Модуль предсталений для обработки и вывода данных на шаблоны
"""
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

import xlwt

from . import models
from . import forms


class ShowPortalPage(UserPassesTestMixin, TemplateView):
    template_name = 'Reserches/index.html'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff


class ShowDevelopView(UserPassesTestMixin, ListView):
    """
    Представление для отображения исследований на стадии разработки
    :attrs:
    model: Пример модели для отображения
    template_name: Название шаблона
    context_object_name: Контекстное имя экемпляра класса Model
    :methods:
    get_queryset(self): Возвращает список исследований
    """
    model = models.Research
    template_name = 'Reserches/develop.html'
    context_object_name = 'posts'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        list_1 = []
        qs1 = models.ImageResearch.objects.filter(base_research__research_state='development')
        qs2 = models.VideoResearch.objects.filter(base_research__research_state='development')
        for el in qs1:
            list_1.append(el)
        for el in qs2:
            list_1.append(el)
        return list_1


class ShowPublishView(UserPassesTestMixin, ListView):
    """
    Предствление для отображения исследований на стадии публикации и завершения
    :attrs:
    model: Пример модели для отображения
    template_name: Название шаблона
    context_object_name: Контекстное имя экземпляра класса Model
    :methods:
    get_queryset(self): Возвращает список исследований
    """
    model = models.Research
    template_name = 'Reserches/published.html'
    context_object_name = 'posts'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        list_1 = []
        qs1 = models.ImageResearch.objects.filter(~Q(base_research__research_state='development'))
        qs2 = models.VideoResearch.objects.filter(~Q(base_research__research_state='development'))
        for el in qs1:
            list_1.append(el)
        for el in qs2:
            list_1.append(el)
        return list_1


class UserLoginView(LoginView):
    """
    Представление для входа пользователя
    :attrs:
    form_class: Класс формы для отображения
    template_name: Название шаблона
    :methods:
    get_success_url(self): Возвращает url для перенаправления при валидации формы
    """
    form_class = forms.LoginUserForm
    template_name = 'Reserches/auth_template.html'
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Войти'
        context['btn_name'] = 'Войти!'
        return context
    
    def get_success_url(self):
        return reverse_lazy('main')


class UserRegisterView(CreateView):
    """
    Представление для регистрации пользователя
    :attrs:
    form_class: Класс формы для отображения
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возврашает url для перенаправления при валидации формы 
    """
    form_class = forms.RegisterUserForm
    template_name = 'Reserches/auth_template.html'
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['btn_name'] = 'Зарегистрироваться!'
        return context
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


def logout_user(request):
    """
    Функция для выхода пользователя
    Возвращает url для перенаправления при выходе
    """
    logout(request)
    return redirect('login')


class CreateResearchView(UserPassesTestMixin, CreateView):
    """
    Предаствление для создания базового исследования
    :attrs:
    form_class: Класс формы для отображения
    template_name: Название шаблона
    :methods:
    form_valid(self): Возвращает url для перенаправления при валидации формы
    """
    form_class = forms.CreateResearchForm
    template_name = 'Reserches/create_base_research.html'
    login_url = '/portal/login'
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание исследования'
        context['btn_name'] = 'Продолжить'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        if form.cleaned_data['ask_published']:
            form.instance.research_state = 'published'
        form.save()
        match form.cleaned_data['research_pattern']:
            case 'image':
                return redirect('image_creation')
            case 'video':
                return redirect('video_creation')
            case _:
                return redirect('index')


def delete_research(request, pk):
    research = get_object_or_404(models.Research, pk=pk)
    if request.method=='POST':
        research.delete()
        return redirect('published')
    return redirect('published')


def finish_research(request, pk):
    research = get_object_or_404(models.Research, pk=pk)
    if request.method=='POST':
        research.research_state = 'done'
        research.save()
        return redirect('published')
    return redirect('published')


class CreateImageResearchView(UserPassesTestMixin, CreateView):
    """
    Представление для создания исследований с шаблоном изображения
    :attrs:
    form_class: Класс формы для отображения
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возврашает url для перенаправления при валидации формы 
    """
    form_class = forms.CreateImageResearchForm
    template_name = 'Reserches/create_research.html'
    login_url = '/portal/login'
    
    def get_context_data(self, *args, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Создание исследования'
            context['btn_name'] = 'Создать исследование!'
            return context
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        form.save()
        return redirect('develop')


class EditImageResearchView(UserPassesTestMixin, UpdateView):
    """
    Предствление для редактирования исследований с шаблоном изображения
    :attrs:
    model: Пример модели для отображения
    context_object_name: Контекстное имя экземпляра класса Model
    pk_url_rwarg: 
    form_class: Класс формы для представления
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возвращает url для перенаправления при валидации формы
    """
    model = models.ImageResearch
    context_object_name = 'research'
    pk_url_kwarg = 'pk'
    form_class = forms.EditImageResearchForm
    template_name = 'Reserches/create_base_research.html'
    login_url = '/portal/login'
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование исследования'
        context['btn_name'] = 'Сохранить!'
        return context
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        base = models.Research.objects.get(id=self.object.base_research.id)
        if form.cleaned_data['ask_published']:
            base.research_state = 'published'
            base.save()
        if form.cleaned_data['research_description']:
            base.research_description = form.cleaned_data['research_description']
        form.save()
        return redirect('develop')


class DetailImageView(UserPassesTestMixin, DetailView):
    """
    
    """
    model = models.ImageResearch
    pk_url_kwarg = 'pk'
    context_object_name = 'research'
    template_name = 'Reserches/detail_template.html'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Просмотр исследования'
        context['btn_name'] = 'Назад'
        context['btn_name_delete'] = 'Удалить исследование'
        context['btn_name_done'] = 'Завершить исследование'
        return context


class CreateVideoResearchView(UserPassesTestMixin, CreateView):
    """
    Представление для создания исследований с шаблоном видео
    :attrs:
    form_class: Класс формы для отображения
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возврашает url для перенаправления при валидации формы 
    """
    form_class = forms.CreateVideoResearchForm
    template_name = 'Reserches/create_research.html'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание исследования'
        context['btn_name'] = 'Создать исследование!'
        return context
    
    def form_valid(self, form):
        form.save()
        return redirect('develop')


class EditVideoResearchView(UserPassesTestMixin, UpdateView):
    """
    Предствление для редактирования исследований с шаблоном видео
    :attrs:
    model: Пример модели для отображения
    context_object_name: Контекстное имя экземпляра класса Model
    pk_url_rwarg: 
    form_class: Класс формы для представления
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возвращает url для перенаправления при валидации формы
    """
    model = models.VideoResearch
    context_object_name = 'research'
    pk_url_kwarg = 'pk'
    form_class = forms.EditVideoResearchForm
    template_name = 'Reserches/create_base_research.html'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование исследования'
        context['btn_name'] = 'Сохранить!'
        return context
    
    def form_valid(self, form):
        base = models.Research.objects.get(id=self.object.base_research.id)
        if form.cleaned_data['ask_published']:
            base.research_state = 'published'
            base.save()
        if form.cleaned_data['research_description']:
            base.research_description = form.cleaned_data['research_description']
        form.save()
        return redirect('develop')
    
    
class DetailVideoView(UserPassesTestMixin, DetailView):
    """
    
    """
    model = models.VideoResearch
    pk_url_kwarg = 'pk'
    context_object_name = 'research'
    template_name = 'Reserches/detail_template.html'
    login_url = '/portal/login'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Просмотр исследования'
        context['btn_name'] = 'Назад'
        context['btn_name_delete'] = 'Удалить исследование'
        context['btn_name_done'] = 'Завершить исследование'
        return context
    
    
def export_image_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Answers')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Имя пользователя', 'Краткий ответ', 'Реакция 1', 'Реакция 2', 'Ощущения от исследования']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = models.ImageResearchAnswer.objects.filter(base_research_answer_id=pk).values_list('respondent_id', 'reaction_text', 'reaction_1', 'reaction_2', 'essence')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response


def export_video_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="export.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Answers')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Имя пользователя', 'Краткий ответ', 'Реакция 1', 'Реакция 2', 'Ощущения от исследования']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = models.VideoResearchAnswer.objects.filter(base_research_answer_id=pk).values_list('respondent_id', 'reaction_text', 'reaction_1', 'reaction_2', 'essence')
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
