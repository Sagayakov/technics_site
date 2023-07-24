from django import template
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from django.db.models import Avg

from technics.models import Category, Technics, UserTechRelation

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


@register.simple_tag
def get_tech_rating(tech_id):
    """Средний рейтинг объекта модели Technics"""

    try:
        technics = Technics.objects.get(id=tech_id)
        rating = technics.usertechrelation_set.aggregate(average_rating=Avg('rating'))['average_rating']
        if rating is None:
            return 'Рейтинг не установлен'
        return round(rating, 2)
    except Technics.DoesNotExist:
        return "Рейтинг не установлен"


@register.simple_tag(takes_context=True)
def get_user_like(context, tech_id):
    """Булевое значение, установлен юзером Лайк на этот объект модели или нет"""

    request = context['request']
    user = request.user
    technics = Technics.objects.get(id=tech_id)
    try:
        user_tech_relation = UserTechRelation.objects.get(user=user, technics=technics)
        return user_tech_relation.like
    except UserTechRelation.DoesNotExist:
        return False


@register.simple_tag(takes_context=True)
def get_user_rating(context, tech_id):
    """Вывод рейтинга на объекте моделе Technics установленный юзером"""

    request = context['request']
    user = request.user
    technics = Technics.objects.get(id=tech_id)
    try:
        user_tech_relation = UserTechRelation.objects.get(user=user, technics=technics)
        return user_tech_relation.rating
    except UserTechRelation.DoesNotExist:
        return False
