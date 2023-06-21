from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

admin.site.register(Comments)


@admin.register(PhotoTech)
class PhotoTechAdmin(admin.ModelAdmin):
    list_display = ['id', 'technic', 'title', 'get_photo']
    fields = ['technic', 'image', 'title']
    list_display_links = ['technic', 'title', 'get_photo']

    def get_photo(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=70>')


@admin.register(Technics)
class TechnicAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'mark', 'model', 'get_photo', 'is_public']
    fields = ['id', 'category', 'get_photo', 'mark', 'model', 'small_description',
              'description', 'photo_main', 'year', 'slug', 'is_public', 'date_create', 'date_update']
    readonly_fields = ['id', 'date_create', 'date_update', 'get_photo']
    list_editable = ['is_public']
    list_display_links = ['id', 'category', 'get_photo']

    def get_photo(self, object):
        if object.photo_main:
            return mark_safe(f'<img src="{object.photo_main.url}" width=70>')

    get_photo.short_description = 'Фото'


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('mark',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category',)}
