from django.core.exceptions import ValidationError
from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    def year_validator(value):
        if value > datetime.datetime.now().year:
            raise ValidationError('Выберите корректный год!')

    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        validators=[year_validator])
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=400, blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles'
    )

    def year_validator(value):
        if value > datetime.datetime.now().year:
            raise ValidationError('Выберите корректный год!')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
