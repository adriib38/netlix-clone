from rest_framework import serializers
from .models import Movie, Serie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['genres'] = [genre['name'] for genre in data['genres']]

        return data


class SerieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Serie
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['genres'] = [genre['name'] for genre in data['genres']]

        return data