from django.db import models
from pytils.translit import slugify
from django.core.validators import MinLengthValidator
from django.urls import reverse


class Category(models.Model):
    """Какой вид техники. Ноутбук/пк или др"""

    category = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(blank=True, db_index=True, unique=True, verbose_name='Ссылка')

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Mark(models.Model):
    """Марка техники. Samsung/lg etc"""

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
    small_description = models.CharField(max_length=200, default='', verbose_name='Краткое описание')
    description = models.TextField(default='', verbose_name='Описание')
    photo_main = models.ImageField(upload_to='photos/technics', verbose_name='Фото', null=True, blank=True)
    # images = models.ForeignKey(PhotoAnimal)
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год выпуска')
    slug = models.SlugField(blank=True, null=True, db_index=True, unique=True, verbose_name='Ссылка')
    is_public = models.BooleanField(default=True, verbose_name='Публикация')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.mark} - {self.model}'

    def get_absolute_url(self):
        return reverse('technic_detail_url', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comments_set.filter(parent__isnull=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.category) + '_' + slugify(self.mark) + '_' + slugify(self.model)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Техники"


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
    technic = models.ForeignKey(Technics, on_delete=models.CASCADE, verbose_name='Техника')
    image = models.ImageField(blank=True, upload_to='photos/technics', verbose_name='Фото')
    title = models.TextField(verbose_name='Описание', default=f'', null=True, blank=True)

    def __str__(self):
        return self.title
