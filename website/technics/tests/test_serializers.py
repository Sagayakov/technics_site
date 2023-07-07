from django.test import TestCase

from technics.serializers import MarkSerializer
from technics.models import *


class TechSerializerTestCase(TestCase):
    def test_mark(self):
        mark_1 = Mark.objects.create(mark='Samsung', slug='samsung')
        mark_2 = Mark.objects.create(mark='LG', slug='lg')

        data = MarkSerializer([mark_1, mark_2], many=True).data

        expected_data = [
            {
                'id': mark_1.id,
                'mark': 'Samsung',
                'slug': 'samsung'
            },
            {
                'id': mark_2.id,
                'mark': 'LG',
                'slug': 'lg'
            }
        ]
        self.assertEqual(expected_data, data)
