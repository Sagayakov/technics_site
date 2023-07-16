import json

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from technics.models import Technics, Mark, Category
from technics.serializers import TechSerializer


class TechApiTestCase(APITestCase):
    """Тестирование API"""

    def setUp(self):
        """Создаем объекты используемые во всем классе"""

        self.user = User.objects.create(username='Test_user')

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
            owner=self.user
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
        """Сравниваем созданные объекты с получаемыми"""

        url = reverse('tech-list')
        response = self.client.get(url)
        serializer_data = TechSerializer([self.technic_1, self.technic_2, self.technic_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        """Проверяем работу поиска по слову Ключевое, ищем в описании"""

        url = reverse('tech-list')
        response = self.client.get(url, data={'search': 'ключевое'})
        serializer_data = TechSerializer([self.technic_2, self.technic_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        """Проверяем фильтрацию по цене"""

        url = reverse('tech-list')
        response = self.client.get(url, data={'price': 1000})
        serializer_data = TechSerializer([self.technic_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_tech_create(self):
        """Проверяем создание нового объекта"""

        self.assertEqual(3, Technics.objects.all().count())

        url = reverse('tech-list')
        data = {
            "model": "Postman",
            "youtube": "www.youtube.com",
            "category": self.category_1.pk,
            "mark": self.mark_1.pk,
            "description": "desc",
            "small_description": "small"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Technics.objects.all().count())
        self.assertEqual(self.user, Technics.objects.last().owner)

    def test_tech_update(self):
        """Обновляем первый объект и проверяем его данные"""

        url = reverse('tech-detail', args=(self.technic_1.id,))
        data = {
            "model": "Postman Edit",
            "youtube": "www.youtube.com",
            "category": self.category_1.pk,
            "mark": self.mark_1.pk,
            "description": "desc",
            "small_description": "small"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user) # авторизация юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.technic_1.refresh_from_db()  # обновление объекта, долго промучился.
        # Объект обновился, а используется старый. Здесь принудительно обновляется.

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Postman Edit", self.technic_1.model)
        self.assertEqual("www.youtube.com", self.technic_1.youtube)
        self.assertEqual("desc", self.technic_1.description)

    def test_tech_delete(self):
        """Проверка удаления объекта"""

        count = Technics.objects.all().count()
        url = reverse('tech-detail', args=(self.technic_1.id,))

        self.client.force_login(self.user)
        response = self.client.delete(url, content_type='application/json')

        self.assertEqual(count - 1, Technics.objects.all().count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_tech_update_not_owner(self):
        """Обновляем данные юзером не создателем объекта, доступа у него нет.
        Данные меняться не должны. Доступ с кодом 403"""

        self.user_2 = User.objects.create(username='Test_user_2')
        url = reverse('tech-detail', args=(self.technic_1.id,))
        data = {
            "model": "Postman Edit",
            "youtube": "www.youtube.com",
            "category": self.category_1.pk,
            "mark": self.mark_1.pk,
            "description": "desc",
            "small_description": "small"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2) # авторизация юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.technic_1.refresh_from_db()  # обновление объекта, долго промучился.
        # Объект обновился, а используется старый. Здесь принудительно обновляется.

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual("Technic1", self.technic_1.model)
        self.assertEqual("Описание полное для техники1", self.technic_1.description)

    def test_tech_update_admin(self):
        """Обновляем данные юзером не создателем объекта, но админом.
        Доступ к изменению чужих данных есть"""

        self.user_2 = User.objects.create(username='Test_user_2', is_staff=True)
        url = reverse('tech-detail', args=(self.technic_1.id,))
        data = {
            "model": "Postman Edit",
            "youtube": "www.youtube.com",
            "category": self.category_1.pk,
            "mark": self.mark_1.pk,
            "description": "desc",
            "small_description": "small"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)  # авторизация юзера
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.technic_1.refresh_from_db()  # обновление объекта, долго промучился.
        # Объект обновился, а используется старый. Здесь принудительно обновляется.

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Postman Edit", self.technic_1.model)
        self.assertEqual("desc", self.technic_1.description)

# copypaste
# coverage run --source='technics' manage.py test technics.tests
# python manage.py test technics.tests.test_api
