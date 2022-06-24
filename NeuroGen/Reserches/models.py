"""Модуль моделей для таблиц БД"""
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Region(models.Model):
    """
    Модель региона
    :attrs:
    region_kod: поле кода региона (является первичным ключом в таблице)
    region_name: поле названия региона
    :methods:
    __str__: возвращает строку для отображения данных при выполнении функции str()
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
        ordering: порядок сортировки данных по полям
    """
    region_kod = models.IntegerField('Код региона', primary_key=True)
    region_name = models.CharField('Регион', max_length=200)

    def __str__(self):
        return f'{self.region_name} ({self.region_kod})'

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering = ['region_kod']


class Customer(models.Model):
    """
    Модель заказчика
    :attrs:
    customer_name: поле названия заказчика
    customer_phone: поле номера телефона заказчика
    customer_date_register: поле даты регистрации заказчика (генерируется автоматически)
    customer_region: поле региона заказчика (связь OneToMany с моделью Region)
    :methods:
    __str__: возвращает строку для отображения данных при выполнении функции str()
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
        ordering: порядок сортировки данных по полям
    """
    customer_name = models.CharField('Наименование заказчика', max_length=100)
    customer_phone = models.CharField('Номер телефона', max_length=16)
    customer_date_register = models.DateTimeField(auto_now_add=True)
    customer_region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer_name)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ['id']


class Research(models.Model):
    """
    Модель базового исследования
    :constants:
    STATES (DEVELOPMENT, PUBLISHED, DONE): стадии исследования
    PATTERNS (PATTERN_1, PATTERN_2): шаблоны исследования
    :attrs:
    research_name: поле названия исследования
    research_customer: поле заказчика исследования (связь OneToMany с моделью Customer)
    research_date_create: поле даты создания исследования (генерируется автоматически)
    research_state: поле состояния исследования (связано с константой STATES)
    research_date_published: поле даты публикации исследования (генерируется автоматически)
    research_pattern: поле шаблона исследования (связано с константой PATTERNS)
    :methods:
    __str__: возвращает строку для отображения данных при выполнении функции str()
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
        ordering: порядок сортировки данных по полям
    """
    DEVELOPMENT = "development"
    PUBLISHED = "published"
    DONE = "done"

    STATES = (
        (DEVELOPMENT, 'Разработка'),
        (PUBLISHED, 'Опубликовано'),
        (DONE, 'Завершено'),
    )
    
    PATTERN_1 = 'image'
    PATTERN_2 = 'video'
    
    PATTERNS = (
        (PATTERN_1, 'Изображение'),
        (PATTERN_2, 'Видео'),
    )
    
    research_name = models.CharField('Название исследования', max_length=100)
    research_customer = models.ForeignKey(Customer, verbose_name='Заказчик', on_delete=models.CASCADE)
    research_date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    research_state = models.CharField(max_length=11, verbose_name='Состояние исследования', choices=STATES, default=DEVELOPMENT)
    research_date_published = models.DateTimeField('Дата публикации', auto_now=True)
    research_pattern = models.CharField(max_length=20, verbose_name='Шаблон исследования', choices=PATTERNS, default=PATTERN_1)
    research_description = models.TextField(verbose_name='Краткое описание', blank=True)

    def __str__(self):
        return self.research_name

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'
        ordering = ['id']


class ImageResearch(models.Model):  
    """
    Модель шаблона изображения
    :attrs:
    base_research: поле ид-р таблицы Изображение
    image_to_rearct: поле содержания файла таблицы Изображение
    :methods:
    __str__(self): возвращает строку для отображения данных при выполнении функции str()
    get_absolute_url(self): Возвращает url опираясь на ид-р таблицы Изображения
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
    """  
    base_research = models.ForeignKey(Research, verbose_name='Основное исследование', on_delete=models.CASCADE)
    image_to_react = models.ImageField(upload_to='img/%Y/%m/%d', verbose_name='Изображение')
    
    def __str__(self):
        return str(self.base_research)
    
    def get_absolute_url(self):
        return reverse('view_image', kwargs={'pk': self.pk})
    
    def get_edit_url(self):
        return reverse("edit_image", kwargs={"pk": self.pk})
    
    def get_answer_url(self):
        return reverse('answer_image', kwargs={'pk': self.pk})    
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'


class ImageResearchAnswer(models.Model):
    """
    Модель ответа Изображение-Ответ
    :constants:
    REACTIONS1 (1, 2, 3): Варианты реакции
    REACTIONS2 (1, 2, 3): Варианты реакции
    :attrs:
    base_research_answer: поле ид-р таблицы Изображение-Ответ
    reaction_text: поле таблицы 
    reaction_1: поле таблицы 
    reaction_2: поле таблицы 
    essense: поле таблицы
    :methods:
    __str__(self): возвращает строку для отображения данных при выполнении функции str()
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
    """
    REACTIONS1 = (
        ('1', 'Я готов за это доплатить'),
        ('2', 'Нравится, но не готов доплатить'),
        ('3', 'Мне это не нравится'),
    )
    
    REACTIONS2 = (
        ('1','Мне это важно'),
        ('2','Мне это НЕ важно'),
        ('3','Я не хочу что бы это было'),
    )
    
    base_research_answer = models.ForeignKey(ImageResearch, verbose_name='Основное исследование', on_delete=models.CASCADE)
    respondent_id = models.CharField('Пользователь', max_length=255)
    reaction_text = models.CharField('Ответ', max_length=255)
    reaction_1 = models.CharField('Эмоция_1', choices=REACTIONS1, max_length=255, default='1')
    reaction_2 = models.CharField('Эмоция_2', choices=REACTIONS2, max_length=255, default='1')
    essence = models.CharField('Покупка', max_length=100)
    # respondent_ids = models.IntegerField('ид-р респондентов',)
    
    def __str__(self):
        return str(self.base_research_answer)    
    
    class Meta:
        verbose_name = 'Изображение Ответ'
        verbose_name_plural = 'Изображение Ответы'



class VideoResearch(models.Model):
    """
    Модель шаблона видео
    :attrs:
    base_research: поле ид-р таблицы Видео
    video_to_rearct: поле содержания файла таблицы Видео
    :methods:
    __str__(self): возвращает строку для отображения данных при выполнении функции str()
    get_absolute_url(self): Возвращает url опираясь на ид-р таблицы Видео
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
    """
    base_research = models.ForeignKey(Research, verbose_name='Основное исследование', on_delete=models.CASCADE)
    video_to_react = models.FileField(upload_to='video/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='Видеоролик',)
    

    def __str__(self):
        return str(self.base_research)
    
    def get_absolute_url(self):
        return reverse('view_video', kwargs={'pk': self.pk})
    
    def get_edit_url(self):
        return reverse("edit_video", kwargs={"pk": self.pk})
    
    def get_answer_url(self):
        return reverse('answer_video', kwargs={'pk': self.pk}) 

    class Meta:
        verbose_name = 'Видеоролик'
        verbose_name_plural = 'Видеоролик'
        
        
class VideoResearchAnswer(models.Model):
    """
    Модель ответа Видео-Ответ
    :constants:
    REACTIONS1 (1, 2, 3): Варианты реакции
    REACTIONS2 (1, 2, 3): Варианты реакции
    :attrs:
    base_research_answer: поле ид-р таблицы Видео-Ответ
    reaction_text: поле таблицы 
    reaction_1: поле таблицы 
    reaction_2: поле таблицы 
    essense: поле таблицы
    :methods:
    __str__(self): возвращает строку для отображения данных при выполнении функции str()
    :subclasses:
    Meta:
        :attrs:
        verbose_name: отображаемое имя модели
        verbose_name_plural: отображаемое имя модели во множественном числе
    """
    REACTIONS1 = (
        ('1', 'Я готов за это доплатить'),
        ('2', 'Нравится, но не готов доплатить'),
        ('3', 'Мне это не нравится'),
    )
    
    REACTIONS2 = (
        ('1','Мне это важно'),
        ('2','Мне это НЕ важно'),
        ('3','Я не хочу что бы это было'),
    )
    
    base_research_answer = models.ForeignKey(VideoResearch, on_delete=models.CASCADE)
    respondent_id = models.CharField('Пользователь', max_length=255)
    reaction_text = models.CharField('Ответ', max_length=255)
    reaction_1 = models.CharField('Эмоция_1', choices=REACTIONS1, max_length=255, default='1')
    reaction_2 = models.CharField('Эмоция_2', choices=REACTIONS2, max_length=255, default='1')
    essence = models.CharField('Покупка', max_length=100)
    
    def __str__(self):
        return str(self.base_research_answer)
    
    class Meta:
        verbose_name = 'Видео Ответ'
        verbose_name_plural = 'Видео Ответы'