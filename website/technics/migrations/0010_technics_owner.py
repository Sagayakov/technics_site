# Generated by Django 4.2.2 on 2023-07-16 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technics', '0009_alter_technics_youtube'),
    ]

    operations = [
        migrations.AddField(
            model_name='technics',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создатель модели'),
        ),
    ]
