from django import template
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

from technics.models import Category, Technics

register = template.Library()


@register.simple_tag()
def get_categories():
    """Достаем все объекты из модели Категории и передаем их в html шаблон.
    Вызывая в html функцию {% get_categories as *** %}"""

    return Category.objects.all().order_by('category')


@register.inclusion_tag('technics/tags/last_tech.html')
def get_last_tech(count=5):
    """Достаем последние добавленные объекты модели Technics.
    Передается в last_tech.html"""

    technic = Technics.objects.order_by('id')[::-1][:count]
    return {'last_tech': technic}


@register.simple_tag(takes_context=True)
def get_name(context):
    """Получаем имя и фамилию юзера при регистрации чз ВК или просто имя"""

    request = context['request']
    user = get_user_model().objects.get(pk=request.user.pk)

    try:
        social_account = SocialAccount.objects.get(user=user, provider='vk')
        user_name = social_account.extra_data.get('first_name')
        user_lastname = social_account.extra_data.get('last_name')
        return f'{user_name} {user_lastname}'
    except SocialAccount.DoesNotExist:
        return user
