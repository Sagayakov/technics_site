from django.db import models
from pytils.translit import slugify
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """Какой вид техники. Ноутбук/пк или др
    slug автоматически заполняется в админ панели,
    здесь не стал забивать функциями"""

    category = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(blank=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Mark(models.Model):
    """Марка техники. Samsung/lg etc
    slug автоматически заполняется в админ панели,
    здесь не стал забивать функциями"""

    mark = models.CharField(max_length=50, verbose_name='Марка')
    slug = models.SlugField(null=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.mark}'

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"


class Technics(models.Model):
    """Основная модель, информация о техники"""

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    mark = models.ForeignKey(Mark, on_delete=models.PROTECT, verbose_name='Марка')
    model = models.CharField(max_length=25, validators=[MinLengthValidator(2)], verbose_name='Модель')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    small_description = models.CharField(max_length=200, default='', verbose_name='Краткое описание')
    description = models.TextField(default='', verbose_name='Описание')
    photo_main = models.ImageField(upload_to='photos/technics', verbose_name='Фото', null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год выпуска')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')
    youtube = models.CharField(max_length=50, help_text='https://www.youtube.com/watch?v=PcIUnpSwhFk')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_tech',
                              verbose_name='Создатель модели')
    clients = models.ManyToManyField(User, through='UserTechRelation', related_name='client_tech',
                                     verbose_name='Взаимодействия')

    def __str__(self):
        return f'{self.mark} - {self.model}'

    def get_absolute_url(self):
        return reverse('technic_detail_url', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comments_set.filter(parent__isnull=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category) + '_' + slugify(self.mark) + '_' + slugify(self.model)
        super().save(*args, **kwargs)

    def get_youtube_link(self):
        try:
            you = self.youtube.split('?v=')[1]
            return str(you)
        except:
            return '0lEaKZhCN-E'

    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Техника"


class Comments(models.Model):
    """Комментарии к модели техники"""

    email = models.EmailField(verbose_name='Email')
    name = models.CharField(max_length=50, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Сообщение')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Родитель')
    technic = models.ForeignKey(Technics, on_delete=models.CASCADE, verbose_name='Техника')

    def __str__(self):
        return f'{self.name} - {self.technic}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class PhotoTech(models.Model):
    """Фотографии к основной моделе Technics"""

    technic = models.ForeignKey(Technics, on_delete=models.CASCADE, verbose_name='Техника')
    image = models.ImageField(blank=True, upload_to='photos/technics', verbose_name='Фото')
    title = models.TextField(verbose_name='Описание', default=f'', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Доп фото Tech"
        verbose_name_plural = "Доп фото Tech"


class UserTechRelation(models.Model):
    """Связь юзера с объектом модели Technics"""

    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    technics = models.ForeignKey(Technics, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, verbose_name='Лайк')
    in_bookmarks = models.BooleanField(default=False, verbose_name='Закладка')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True)

    def __str__(self):
        return f'{self.user}: {self.technics}, rating {self.rating}'

    class Meta:
        verbose_name = "Взаимодействие пользователя"
        verbose_name_plural = "Взаимодействия пользователей"
