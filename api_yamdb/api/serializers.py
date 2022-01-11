import datetime as dt

from categories.models import Categories, Genres, Title
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Comment, Review
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'It is forbidden to use this name as a username.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id', 'password', 'last_login', 'is_staff', 'is_active',
                   'is_superuser', 'groups', 'date_joined', 'user_permissions')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        exclude = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review', )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title', )

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data

        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'You can only leave one review '
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'enter a score from 1 to 10 '
            )
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id', )


class CreateTitleSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genres.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value <= dt.datetime.now().year:
            return value
        raise serializers.ValidationError(
            'Год выпуска не может быть '
            'больше текущего!'
        )

    def validate_category(self, value):
        if not Categories.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Категории с таким slug '
                'не существует'
            )
        return value

    def validate_genre(self, value):
        for genre in value:
            if not Genres.objects.filter(slug=genre).exists():
                raise serializers.ValidationError(
                    'Жанра с таким slug '
                    'не существует'
                )
        return value


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return None
        return round(rating)
