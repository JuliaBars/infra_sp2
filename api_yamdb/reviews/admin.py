from django.contrib import admin
from django.contrib.auth.models import Group

from reviews.models import Category, Comment, Genre, Review, Title

admin.site.register(Category)
admin.site.register(Genre)
admin.site.unregister(Group)


class TitleInlineAdmin(admin.TabularInline):
    model = Title.genre.through
    min_num = 1
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [TitleInlineAdmin]
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'text', 'pub_date', 'score')
    search_fields = ('title', 'author',)
    list_filter = ('author', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('review', 'author',)
    list_filter = ('author',)
