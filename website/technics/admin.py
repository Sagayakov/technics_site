from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class TechAdminForm(forms.ModelForm):
    """CK Editor. Возможность редактирования вывода description"""

    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание')

    class Meta:
        model = Technics
        fields = '__all__'



@admin.register(PhotoTech)
class PhotoTechAdmin(admin.ModelAdmin):
    """Фотографии к моделе Tech"""

    list_display = ['id', 'technic', 'title', 'get_photo']
    fields = ['technic', 'image', 'title']
    list_display_links = ['technic', 'title', 'get_photo']

    def get_photo(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=70>')


class CommentsInLine(admin.TabularInline):
    """Добавление комментариев в админ Tech"""
    model = Comments
    readonly_fields = ['name', 'email', 'text', 'parent', 'technic']
    extra = 0


class PhotoTechInLine(admin.StackedInline):
    """Добавление доп фото на страницу Tech"""

    model = PhotoTech
    extra = 1
    readonly_fields = ['get_photo']

    def get_photo(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=150>')


@admin.register(Technics)
class TechnicAdmin(admin.ModelAdmin):
    """Основная модель техники"""

    list_display = ['id', 'category', 'mark', 'model', 'get_photo', 'is_public']
    fields = ['id', 'category', 'get_photo', 'mark', 'model', 'price', 'small_description',
              'description', 'photo_main', 'year', 'slug', 'youtube', 'is_public',
              'date_create', 'date_update']
    readonly_fields = ['id', 'date_create', 'date_update', 'get_photo']
    list_editable = ['is_public']
    list_display_links = ['id', 'category', 'get_photo']
    list_filter = ['category', 'year']
    search_fields = ['model']
    inlines = [CommentsInLine, PhotoTechInLine]
    form = TechAdminForm
    actions = ['publish', 'un_publish']

    def get_photo(self, object):
        if object.photo_main:
            return mark_safe(f'<img src="{object.photo_main.url}" width=70>')

    def publish(self, request, queryset):
        """Action действие. Опубликовать"""

        row_update = queryset.update(is_public=True)
        if row_update == 1:
            message_bit = '1 запись обновленна'
        else:
            message_bit = f'{row_update} записей было обновленно'
        self.message_user(request, f'{message_bit}')

    def un_publish(self, request, queryset):
        """Action действие. Снять с публикации"""

        row_update = queryset.update(is_public=False)
        if row_update == 1:
            message_bit = '1 запись обновленна'
        else:
            message_bit = f'{row_update} записей было обновленно'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    un_publish.short_description = 'Снять с публикации'
    un_publish.allowed_permissions = ('change',)

    get_photo.short_description = 'Фото'


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Комментарии"""

    list_display = ['name', 'email', 'parent']
    readonly_fields = ['name', 'email', 'text', 'parent', 'technic']


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    """Марка техники"""

    prepopulated_fields = {'slug': ('mark',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категория техники. Ноут/ПК или др"""

    prepopulated_fields = {'slug': ('category',)}
