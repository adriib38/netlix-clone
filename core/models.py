from django.db import models
import uuid
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator 
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


# Create your models here.
class Genre(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    genres = models.ManyToManyField(Genre, null=False)
    duration_min = models.IntegerField(null=True)
    cover_image = models.ImageField(
        upload_to='movie_images', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        help_text="Cover Image",
        null=True
    )
    video = models.FileField(
        upload_to='movie_videos',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
    )
    views = models.IntegerField(default = 0)
    

    def __str__(self):
        return self.title
    
class Serie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    genres = models.ManyToManyField(Genre, null=False)
    cover_image = models.ImageField(
        upload_to='movie_images', 
        height_field=None, 
        width_field=None, 
        max_length=100, 
        help_text="Cover Image",
        null=True
    )
    views = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.title
    
class Season(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    n_season = models.IntegerField()
    def __str__(self):
        return self.serie.title + ' / Season ' + str(self.n_season)

class Chapter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    duration_min = models.IntegerField(null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to='movie_videos',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
    )
    def __str__(self):
        return self.title

class ListContent(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'List: ' + self.user.username

class Content(PolymorphicModel):
    list_content = models.ForeignKey(ListContent, on_delete=models.SET_NULL, null=True)

class MovieContent(Content):
    # Atributos específicos de contenido de película
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  
    content_type = models.CharField(max_length=255, default='movie')

class SerieContent(Content):
    # Atributos específicos de contenido de serie
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)

    content_type = models.CharField(max_length=255, default='serie')