from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )
    rating = serializers.IntegerField(read_only=True)
    category = Category(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value

    # def to_representation(self, instance): #  Это то что он отдает?, а надо чтобы не принимал
    #     if self.context.get('request').method == 'POST':
    #         return {
    #             "name": instance.name,
    #             "year": instance.year,
    #             "description": instance.description,
    #             "genre": instance.genre,
    #             "category": instance.category
    #         }
    #     return super().to_representation(instance)
