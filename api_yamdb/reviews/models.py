from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=400, blank=True, null=True)
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='title'
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='title'
    )

    def __str__(self):
        return self.name
