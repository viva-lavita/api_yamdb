from rest_framework import serializers
from reviews.models import Comment, Review

MIN_VALUE = 1
MAX_VALUE = 10


class CategorySerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    score = serializers.IntegerField(
        min_value=MIN_VALUE, max_value=MAX_VALUE
    )

    def validate(self, data):
        super().validate(data)

        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title__id=title_id).exists():
            raise serializers.ValidationError("Автор уже оставлял отзыв")
        return data

    class Meta:
        model = Review
        field = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        field = '__all__'
