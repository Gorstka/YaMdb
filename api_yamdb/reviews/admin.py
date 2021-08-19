from django.contrib import admin

from .models import Category, Genre, Title


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoriesAdmin)
admin.site.register(Genre, GenresAdmin)
admin.site.register(Title, TitlesAdmin)
