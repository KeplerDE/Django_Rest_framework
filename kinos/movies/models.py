from django.db import models
from datetime import date

from django.urls import reverse

class Category(models.Model):
    """Kategorien"""
    name = models.CharField("Kategorie", max_length=150)
    description = models.TextField("Beschreibung")
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

class Actor(models.Model):
    """Akteuren und Regisseure"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Alter", default=0)
    description = models.TextField("Beschreibung")
    image = models.ImageField("Bildschirmbild", upload_to="actors/")


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Akteuren und Regisseure"
        verbose_name_plural = "Akteuren und Regisseure"


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Beschreibung")
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"



class Movie(models.Model):
    """Kino"""
    title = models.CharField("Name", max_length=100)
    tagline = models.CharField("Slogan", max_length=100, default='')
    description = models.TextField("Beschreibung")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Veröffentlichungsdatum", default=2019)
    country = models.CharField("Land", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="Regisseure", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Akteuren", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("Premiere in der Welt", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="Die Summe im Euro zu bezeichnen")
    fees_in_usa = models.PositiveSmallIntegerField(
        "Gebühren in USA", default=0, help_text="Die Summe im Euro zu bezeichnen"
    )
    fees_in_world = models.PositiveIntegerField(
        "Gebühren in Welt", default=0, help_text="Die Summe im Euro zu bezeichnen"
    )
    category = models.ForeignKey(
        Category, verbose_name="Kategorie", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Konzept", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filme"

class MovieShots(models.Model):
    """Die Fachkräfte aus dem Film"""
    title = models.CharField("Titel", max_length=100)
    description = models.TextField("Beschreibung")
    image = models.ImageField("Bildschirmbild", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Film", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Die Fachkraft aus dem Film"
        verbose_name_plural = "Die Fachkräfte aus dem Film"



class RatingStar(models.Model):
    """Stars"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Der Stern des Ratings"
        verbose_name_plural = "Die Sterne des Ratings"
        ordering = ["value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Star")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Film")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"




