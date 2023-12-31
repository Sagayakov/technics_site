# Generated by Django 4.2.2 on 2023-06-25 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technics', '0003_alter_phototech_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
            },
        ),
        migrations.AlterModelOptions(
            name='technics',
            options={'verbose_name': 'Техника', 'verbose_name_plural': 'Техника'},
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='IP')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technics.ratingstar', verbose_name='Звезда')),
                ('technic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technics.technics', verbose_name='Техника')),
            ],
        ),
    ]
