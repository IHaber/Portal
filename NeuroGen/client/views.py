from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


from Reserches import models
from . import forms


class ShowMainPage(TemplateView):
    template_name = 'client/index.html'


class ShowAvailiableResearchesView(LoginRequiredMixin, ListView):
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
    template_name = 'client/list_research.html'
    context_object_name = 'posts'
    login_url = 'portal/login'
    
    def get_queryset(self):
        list_1 = []
        qs1 = models.ImageResearch.objects.filter(Q(base_research__research_state='published'))
        qs2 = models.VideoResearch.objects.filter(Q(base_research__research_state='published'))
        for el in qs1:
            list_1.append(el)
        for el in qs2:
            list_1.append(el)
        return list_1
    
    
    
class AnswerImageResearchView(DetailView, CreateView):
    """
    Представление для создания исследований с шаблоном изображения
    :attrs:
    form_class: 
    template_name: Название шаблона
    :methods:
    form_valid(self, for    m): Возврашает url для перенаправления при валидации формы 
    """
    model = models.ImageResearch
    context_object_name = 'answer_research'
    pk_url_kwarg = 'pk'
    form_class = forms.AnswerImageResearchForm
    template_name = 'client/answer_page.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ответ на исследования'
        context['btn_name'] = 'Завершить исследование!'
        return context

    def form_valid(self, form):
        form.instance.base_research_answer = self.get_object()
        form.instance.respondent_id = self.request.user.username
        form.save()
        return redirect('researches')
    
    
class AnswerVideoResearchView(DetailView, CreateView):
    """
    Представление для создания исследований с шаблоном изображения
    :attrs:
    form_class: 
    template_name: Название шаблона
    :methods:
    form_valid(self, form): Возврашает url для перенаправления при валидации формы 
    """
    model = models.VideoResearch
    context_object_name = 'answer_research'
    pk_url_kwarg = 'pk'
    form_class = forms.AnswerVideoResearchForm
    template_name = 'client/answer_page.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ответ на исследования'
        context['btn_name'] = 'Завершить исследование!'
        return context

    def form_valid(self, form):
        form.instance.base_research_answer = self.get_object()
        form.instance.respondent_id = self.request.user.username
        form.save()
        return redirect('researches')