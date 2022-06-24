# Generated by Django 4.0.4 on 2022-06-13 11:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100, verbose_name='Наименование заказчика')),
                ('customer_phone', models.CharField(max_length=16, verbose_name='Номер телефона')),
                ('customer_date_register', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Заказчик',
                'verbose_name_plural': 'Заказчики',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ImageResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_to_react', models.ImageField(upload_to='img/%Y/%m/%d', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображение',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_kod', models.IntegerField(primary_key=True, serialize=False, verbose_name='Код региона')),
                ('region_name', models.CharField(max_length=200, verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'ordering': ['region_kod'],
            },
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_name', models.CharField(max_length=100, verbose_name='Название исследования')),
                ('research_date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('research_state', models.CharField(choices=[('development', 'Разработка'), ('published', 'Опубликовано'), ('done', 'Завершено')], default='development', max_length=11, verbose_name='Состояние исследования')),
                ('research_date_published', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('research_pattern', models.CharField(choices=[('image', 'Изображение'), ('video', 'Видео')], default='image', max_length=20, verbose_name='Шаблон исследования')),
                ('research_description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('research_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.customer', verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Исследование',
                'verbose_name_plural': 'Исследования',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='VideoResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_to_react', models.FileField(upload_to='video/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='Видеоролик')),
                ('base_research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.research', verbose_name='Основное исследование')),
            ],
            options={
                'verbose_name': 'Видеоролик',
                'verbose_name_plural': 'Видеоролик',
            },
        ),
        migrations.CreateModel(
            name='VideoResearchAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondent_id', models.CharField(max_length=255, verbose_name='Пользователь')),
                ('reaction_text', models.CharField(max_length=255, verbose_name='Ответ')),
                ('reaction_1', models.CharField(choices=[('1', 'Я готов за это доплатить'), ('2', 'Нравится, но не готов доплатить'), ('3', 'Мне это не нравится')], default='1', max_length=255, verbose_name='Эмоция_1')),
                ('reaction_2', models.CharField(choices=[('1', 'Мне это важно'), ('2', 'Мне это НЕ важно'), ('3', 'Я не хочу что бы это было')], default='1', max_length=255, verbose_name='Эмоция_2')),
                ('essence', models.CharField(max_length=100, verbose_name='Покупка')),
                ('base_research_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.videoresearch')),
            ],
            options={
                'verbose_name': 'Видео Ответ',
                'verbose_name_plural': 'Видео Ответы',
            },
        ),
        migrations.CreateModel(
            name='ImageResearchAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondent_id', models.CharField(max_length=255, verbose_name='Пользователь')),
                ('reaction_text', models.CharField(max_length=255, verbose_name='Ответ')),
                ('reaction_1', models.CharField(choices=[('1', 'Я готов за это доплатить'), ('2', 'Нравится, но не готов доплатить'), ('3', 'Мне это не нравится')], default='1', max_length=255, verbose_name='Эмоция_1')),
                ('reaction_2', models.CharField(choices=[('1', 'Мне это важно'), ('2', 'Мне это НЕ важно'), ('3', 'Я не хочу что бы это было')], default='1', max_length=255, verbose_name='Эмоция_2')),
                ('essence', models.CharField(max_length=100, verbose_name='Покупка')),
                ('base_research_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.imageresearch', verbose_name='Основное исследование')),
            ],
            options={
                'verbose_name': 'Изображение Ответ',
                'verbose_name_plural': 'Изображение Ответы',
            },
        ),
        migrations.AddField(
            model_name='imageresearch',
            name='base_research',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.research', verbose_name='Основное исследование'),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Reserches.region', verbose_name='Регион'),
        ),
    ]
