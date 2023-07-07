from rest_framework.serializers import ModelSerializer

from technics.models import Technics, Mark, Category


class TechSerializer(ModelSerializer):
    class Meta:
        model = Technics
        fields = '__all__'


class MarkSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
