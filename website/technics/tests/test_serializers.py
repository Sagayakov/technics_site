from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from technics.serializers import MarkSerializer, CategorySerializer, TechSerializer
from technics.models import *
from technics.templatetags.technic_tag import get_tech_rating


class TechSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='user_1')
        self.user_2 = User.objects.create(username='user_2')
        self.user_3 = User.objects.create(username='user_3')

        self.mark_1 = Mark.objects.create(mark='Mark1', slug='mark1')
        self.mark_2 = Mark.objects.create(mark='Mark2', slug='mark2')

        self.category_1 = Category.objects.create(category='Category1', slug='category1')
        self.category_2 = Category.objects.create(category='Category2', slug='category2')

        self.technic_1 = Technics.objects.create(
            category=self.category_1,
            mark=self.mark_1,
            model='Technic1',
            year=2020,
            price=1000,
            small_description='Техника1',
            description='Описание полное для техники1',
            is_public=True,
            photo_main=None
        )
        self.technic_2 = Technics.objects.create(
            category=self.category_2,
            mark=self.mark_2,
            model='Technic2',
            year=2022,
            price=100,
            small_description='Техника2',
            description='Описание полное для техники2. Ключевое слово',
            is_public=True,
            photo_main=None
        )
        self.technic_3 = Technics.objects.create(
            category=self.category_1,
            mark=self.mark_2,
            model='Technic3',
            year=2019,
            price=700,
            small_description='Техника3 ключевое',
            description='Описание полное для техники3',
            is_public=True,
            photo_main=None
        )

    def test_mark(self):
        """Проверка создания объектов модели Mark"""

        data = MarkSerializer([self.mark_1, self.mark_2], many=True).data

        expected_data = [
            {
                'id': self.mark_1.id,
                'mark': 'Mark1',
                'slug': 'mark1'
            },
            {
                'id': self.mark_2.id,
                'mark': 'Mark2',
                'slug': 'mark2'
            }
        ]
        self.assertEqual(expected_data, data)

    def test_category(self):
        """Проверка создания объектов модели Category"""

        data = CategorySerializer([self.category_1, self.category_2], many=True).data

        expected_data = [
            {
                'id': self.category_1.id,
                'category': 'Category1',
                'slug': 'category1'
            },
            {
                'id': self.category_2.id,
                'category': 'Category2',
                'slug': 'category2'
            }
        ]
        self.assertEqual(expected_data, data)

    def test_relation(self):
        """Проверка связи между юзером и объектом модели Technics"""

        UserTechRelation.objects.create(
            user=self.user_1, technics=self.technic_1, like=True, in_bookmarks=True, rating=4
        )
        UserTechRelation.objects.create(
            user=self.user_2, technics=self.technic_1, like=True, in_bookmarks=True, rating=3
        )
        UserTechRelation.objects.create(
            user=self.user_3, technics=self.technic_1, like=False, in_bookmarks=True, rating=5
        )
        UserTechRelation.objects.create(
            user=self.user_3, technics=self.technic_3, like=True, rating=2
        )
        # serializer_1 = TechSerializer(self.technic_1)
        # serializer_2 = TechSerializer(self.technic_3)

        tech = Technics.objects.all().annotate(
            likes_annotated=Count(Case(When(usertechrelation__like=True, then=1))),
            rating_annotated=Avg('usertechrelation__rating')
        ).order_by('id')

        first_tech = tech.first()
        second_tech = tech[1]
        third_tech = tech[2]

        data_serializer = TechSerializer(tech, many=True).data

        # тестирование не только сериализатора, для наглядности засунул все в один тест,
        # получение рейтинга и лайков разными способами

        self.assertTrue(UserTechRelation.objects.filter(user=self.user_1, technics=self.technic_1).exists())
        self.assertEqual(2, data_serializer[0]['likes_annotated'])
        self.assertEqual(2, first_tech.likes_annotated)
        self.assertEqual(1, data_serializer[2]['likes_annotated'])
        self.assertEqual(1, third_tech.likes_annotated)
        self.assertEqual('4.00', data_serializer[0]['rating_annotated'])
        self.assertEqual(4, first_tech.rating_annotated)
        self.assertEqual(4, get_tech_rating(self.technic_1.id))
        self.assertEqual('2.00', data_serializer[2]['rating_annotated'])
        self.assertEqual(2, third_tech.rating_annotated)
        self.assertEqual(None, second_tech.rating_annotated)
        self.assertEqual(None, data_serializer[1]['rating_annotated'])
        self.assertTrue(self.technic_1.usertechrelation_set.filter(user=self.user_1, in_bookmarks=True))
        self.assertFalse(self.technic_3.usertechrelation_set.filter(user=self.user_3, in_bookmarks=True))
