from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from technics.models import Technics, Mark, Category, UserTechRelation


class TechClientsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class TechSerializer(ModelSerializer):
    # likes_count = serializers.SerializerMethodField()
    likes_annotated = serializers.IntegerField(read_only=True)
    rating_annotated = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    clients = TechClientsSerializer(many=True, read_only=True)

    class Meta:
        model = Technics
        fields = (
            'id', 'mark', 'model', 'price', 'small_description', 'description',
            'year', 'category', 'slug', 'youtube', 'is_public', 'likes_annotated',
            'rating_annotated', 'owner_name', 'clients'
        )

    # def get_likes_count(self, instance):
    #     return UserTechRelation.objects.filter(technics=instance, like=True).count()


class MarkSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserTechRelationSerializer(ModelSerializer):
    class Meta:
        model = UserTechRelation
        fields = ('technics', 'like', 'in_bookmarks', 'rating')
