from django import template

from technics.models import Category, Technics

register = template.Library()


@register.simple_tag()
def get_categories():
    """Достаем все объекты из модели Категории и передаем их в html шаблон.
    Вызывая в html функцию {% get_categories as *** %}"""

    return Category.objects.all()


@register.inclusion_tag('technics/tags/last_tech.html')
def get_last_tech(count=5):
    """Достаем последние добавленные объекты модели Technics.
    Передается в last_tech.html"""

    technic = Technics.objects.order_by('id')[::-1][:count]
    return {'last_tech': technic}
