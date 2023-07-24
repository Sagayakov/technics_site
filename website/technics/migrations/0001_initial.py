# Generated by Django 4.2.2 on 2023-06-20 13:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, verbose_name='Категория')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=50, verbose_name='Марка')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Марка',
                'verbose_name_plural': 'Марки',
            },
        ),
        migrations.CreateModel(
            name='Technics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=25, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Модель')),
                ('small_description', models.CharField(default='', max_length=200, verbose_name='Краткое описание')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('photo_main', models.ImageField(blank=True, null=True, upload_to='photos/technics', verbose_name='Фото')),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Год выпуска')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Ссылка')),
                ('is_public', models.BooleanField(default=True, verbose_name='Публикация')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='technics.category', verbose_name='Категория')),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='technics.mark', verbose_name='Марка')),
            ],
            options={
                'verbose_name': 'Техника',
                'verbose_name_plural': 'Техники',
            },
        ),
        migrations.CreateModel(
            name='PhotoTech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='photos/technics', verbose_name='Фото')),
                ('title', models.TextField(default='', verbose_name='Описание')),
                ('technic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technics.technics', verbose_name='Техника')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='technics.comments', verbose_name='Родитель')),
                ('technic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technics.technics', verbose_name='Техника')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]