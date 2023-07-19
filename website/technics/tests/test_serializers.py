from django.test import TestCase

from technics.serializers import MarkSerializer, CategorySerializer, TechSerializer
from technics.models import *


class TechSerializerTestCase(TestCase):
    def setUp(self):
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
        user_1 = User.objects.create(username='user_1')
        user_2 = User.objects.create(username='user_2')
        user_3 = User.objects.create(username='user_3')

        UserTechRelation.objects.create(
            user=user_1, technics=self.technic_1, like=True, in_bookmarks=True, rating=4
        )
        UserTechRelation.objects.create(
            user=user_2, technics=self.technic_1, like=True, in_bookmarks=True, rating=3
        )
        UserTechRelation.objects.create(
            user=user_3, technics=self.technic_3, like=True, in_bookmarks=True, rating=2
        )
        serializer = TechSerializer(self.technic_1)
        self.assertTrue(UserTechRelation.objects.filter(user=user_1, technics=self.technic_1).exists())
        self.assertEqual(2, serializer.data['likes_count'])

