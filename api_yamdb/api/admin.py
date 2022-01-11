from categories.models import Categories, Genres, Title
from django.contrib import admin
from reviews.models import Comment, Review
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'role')
    search_fields = ('username', )
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'category', 'rating'
    )
    list_filter = ('category', )
    search_fields = ('name', )
    ordering = ('year', 'rating')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
