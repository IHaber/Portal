from cProfile import label
from django import forms

from Reserches import models


class AnswerImageResearchForm(forms.ModelForm):
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
    reaction_text = forms.CharField(
        label='Краткий ответ:',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    reaction_1 = forms.ChoiceField(
        label='Реакция 1',
        choices=models.ImageResearchAnswer.REACTIONS1,
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    reaction_2 = forms.ChoiceField(
        label='Реакция 2',
        choices=models.ImageResearchAnswer.REACTIONS2,
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    essence = forms.CharField(
        label='Ваши ощущения',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control shadow-sm rounded'
                }
            )
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reaction_1'].empty_label = 'Выберите ответ:'
        self.fields['reaction_2'].empty_label = 'Выберите ответ:'
    
    class Meta:
        model = models.ImageResearchAnswer
        fields = ['reaction_text', 'reaction_1', 'reaction_2', 'essence' ]
        
        
class AnswerVideoResearchForm(forms.ModelForm):
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
    reaction_text = forms.CharField(label='Краткий ответ:')
    reaction_1 = forms.ChoiceField(
        label='Реакция 1',
        choices=models.VideoResearchAnswer.REACTIONS1,
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    reaction_2 = forms.ChoiceField(
        label='Реакция 2',
        choices=models.VideoResearchAnswer.REACTIONS2,
        widget=forms.Select(
            attrs={
                'class': 'form-select shadow-sm rounded'
                }
            )
        )
    essence = forms.CharField(label='Ваши ощущения')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reaction_1'].empty_label = 'Выберите ответ:'
        self.fields['reaction_2'].empty_label = 'Выберите ответ:'
    
    class Meta:
        model = models.VideoResearchAnswer
        fields = ['reaction_text', 'reaction_1', 'reaction_2', 'essence' ]