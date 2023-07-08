from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from technics.models import Technics, Mark, Category
from technics.serializers import TechSerializer


class TechApiTestCase(APITestCase):

    from technics.views import TechViewSet
    TechViewSet.permission_classes = []

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
            is_public=True
        )
        self.technic_2 = Technics.objects.create(
            category=self.category_2,
            mark=self.mark_2,
            model='Technic2',
            year=2022,
            price=100,
            small_description='Техника2',
            description='Описание полное для техники2. Ключевое слово',
            is_public=True
        )
        self.technic_3 = Technics.objects.create(
            category=self.category_1,
            mark=self.mark_2,
            model='Technic3',
            year=2019,
            price=700,
            small_description='Техника3 ключевое',
            description='Описание полное для техники3',
            is_public=True
        )

    def test_get(self):
        url = reverse('tech-list')
        response = self.client.get(url)
        serializer_data = TechSerializer([self.technic_1, self.technic_2, self.technic_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('tech-list')
        response = self.client.get(url, data={'search': 'ключевое'})
        serializer_data = TechSerializer([self.technic_2, self.technic_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('tech-list')
        response = self.client.get(url, data={'price': 1000})
        serializer_data = TechSerializer([self.technic_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

# copypaste
# coverage run --source='technics' manage.py test technics.tests
# python manage.py test technics.tests.test_api
