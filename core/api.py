# core/api.py
from rest_framework import viewsets
from .models import Movie, Serie
from .serializers import MovieSerializer, SerieSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    def retrieve(self, request, pk=None):
        movie = get_object_or_404(Movie, uuid=pk)
        serializer = self.get_serializer(movie)
        return Response(serializer.data)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer

    
    def retrieve(self, request, pk=None):
        serie = get_object_or_404(Serie, uuid=pk)
        serializer = self.get_serializer(serie)
        return Response(serializer.data)

