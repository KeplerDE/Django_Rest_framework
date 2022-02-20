from django.db import models
from rest_framework import generics


from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip

class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies
#переделали на метод get_queryset

class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer

# также переделали

class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer

#переписали указали класс сериализации


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


#такая же история только созраняем ай пи адрес и селф мы принимаем через request

class ActorsListView(generics.ListAPIView):   #наследуемся от джнерика
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Вывод актера или режиссера"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer