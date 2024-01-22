from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import re
from django.http import JsonResponse
from .models import Movie, Serie, Season, Chapter, Genre, ListContent, MovieContent, SerieContent, Content
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import F
from django.db.models import Q, Subquery
import json


def index(request):

   header_movie = Movie.objects.all().first()

   listUser = ListContent.objects.filter(user_id=request.user.id).first()
   content = Content.objects.filter(list_content=listUser)

   # Obtener todos los géneros
   genres = Genre.objects.all()

   # Obtener todas las películas y series
   movies = Movie.objects.all()
   series = Serie.objects.all()

   # Crear una estructura de datos para pasar a la plantilla
   data = {"genres": []}

   for genre in genres:
      # Filtrar películas y series por género
      genre_movies = movies.filter(genres=genre)
      genre_series = series.filter(genres=genre)

      # Crear datos para el género actual
      genre_data = {
         "name": genre.name,
         "movies": [
            {
               "id": movie.id,
               "title": movie.title,
               "duration": movie.duration_min,
               "uuid": movie.uuid,
               "cover_image": movie.cover_image.url if movie.cover_image else None,
            } for movie in genre_movies
         ],
         "series": [
            {
               "id": serie.id,
               "title": serie.title,
               "uuid": serie.uuid,
               "cover_image": serie.cover_image.url if serie.cover_image else None,
            } for serie in genre_series
         ],
      }

      # Agregar datos del género a la lista
      data["genres"].append(genre_data)

   moviesNoGenre = Movie.objects.filter(genres__isnull=True)
   seriesNoGenre = Serie.objects.filter(genres__isnull=True)

   context = {
      'genres': data,
      'moviesNoGenre': moviesNoGenre,
      'seriesNoGenre': seriesNoGenre,
      'header_movie': header_movie,
      'list': content
   }
   return render(request, 'index.html', context)

 
 
def login(request):
   if request.method == 'GET':
      return render(request, 'auth/login.html', {
         'form': AuthenticationForm(),
      })
   elif request.method == 'POST':
      try:
         user = User.objects.get(username=request.POST['username'])
         
         if user.check_password(request.POST['password']):
            print('Login succesfull')
            auth_login(request, user)
            response = redirect('/')
            return response
         else: 
            return render(request, 'auth/login.html', {
               'form': AuthenticationForm(),
               'error': 'Password not correct'
            })
      except User.DoesNotExist:
         return render(request, 'auth/login.html', {
            'form': AuthenticationForm(),
            'error': 'No account has been found with this email address. Try again or <a href="/register">create a new account.</a>'
         })

def subscribe(request):
   if request.method == 'GET':
      return render(request, 'auth/subscribe.html', {
         'form': UserCreationForm(),
      })
   elif request.method == 'POST':
      if request.POST['password1'] == request.POST['password2']:
         try:
            validate_password(request.POST['password1'])
         except ValidationError as e:
            return render(request, 'auth/subscribe.html', {
               'form': UserCreationForm(),
               'error': e.messages[0],
            })
         try:
            user = User.objects.create_user(
               username=request.POST['username'],
               password=request.POST['password1'],
            )
            user.save()
            
            auth_login(request, user)
            response = redirect('/')
            return response
         except IntegrityError:
            return render(request, 'auth/subscribe.html', {
               'form': UserCreationForm(),
               'error': 'Error'
            })
      else:
         return render(request, 'auth/subscribe.html', {
            'form': UserCreationForm(),
            'error': 'Pass not mtch'
         })

@login_required(login_url='/login')
def movies(request):

   genres = Genre.objects.filter(movie__isnull=False).distinct()
   movies = Movie.objects.all()
   moviesNoGenre = Movie.objects.filter(genres__isnull=True)

   data = {"genres": []}
   for genre in genres:
      genre_movies = movies.filter(genres=genre)
      genre_data = {
         "name": genre.name,
         "movies": [
            {
               "title": movie.title, 
               "duration": movie.duration_min,
               "uuid": movie.uuid,
               "cover_image": movie.cover_image,
            } for movie in genre_movies
         ],
      }
      data["genres"].append(genre_data)
      genre_movies = []

   context = {
      'genres': data,
      'moviesNoGenre': moviesNoGenre
   }
   return render(request, 'movies.html', context)

@login_required(login_url='/login')
def movie(request, movie_uuid):
   movie = Movie.objects.filter(uuid=movie_uuid).first()
   listUser = ListContent.objects.filter(user_id=request.user.id).first()

   movieInList = MovieContent.objects.filter(list_content=listUser, movie_id=movie).exists()

   Movie.objects.filter(uuid=movie_uuid).update(views=F('views')+1)
   context = {
      'movie': movie,
      'movieInList': movieInList
   }
   return render(request, 'movie.html', context)

@login_required(login_url='/login')
def series(request):
   genres = Genre.objects.filter(serie__isnull=False).distinct()
   series = Serie.objects.all()
   seriesNoGenre = Serie.objects.filter(genres__isnull=True)

   data = {"genres": []}
   for genre in genres:
      genre_movies = series.filter(genres=genre)
      genre_data = {
         "name": genre.name,  # Agrega los campos específicos que necesitas
         "series": [
            {
               "title": movie.title, 
               "uuid": movie.uuid,
               "cover_image": movie.cover_image,
            } for movie in genre_movies
         ],
      }
      data["genres"].append(genre_data)
      genre_movies = []


   context = {
      'genres': data,
      'seriesNoGenre': seriesNoGenre
   }
   return render(request, 'series.html', context)

@login_required(login_url='/login')
def chapter(request, chapter_uuid):

   chapter = Chapter.objects.filter(uuid=chapter_uuid).first()
   serie = chapter.season.serie
   season = chapter.season

   context = {
      'chapter': chapter,
      'serie': serie,
      'season': season,
   }
   return render(request, 'chapter.html', context)


@login_required(login_url='/login')
def serie(request, serie_uuid):
   serie = Serie.objects.filter(uuid=serie_uuid).first()
   seasons = Season.objects.filter(serie=serie)

   serie_data = {}
   for season in seasons:
      chapters = Chapter.objects.filter(season=season)

      serie_data[season] = chapters

   Serie.objects.filter(uuid=serie_uuid).update(views=F('views')+1)
   listUser = ListContent.objects.filter(user_id=request.user.id).first()
   serieInList = SerieContent.objects.filter(list_content=listUser, serie_id=serie).exists()

   context = {
      'serie': serie,
      'serie_data': serie_data,
      'serieInList': serieInList,
   }
   return render(request, 'serie.html', context)


@login_required(login_url='/login')
def toggleToList(request, typevideo, uuid):
   
   if typevideo == 'movie':
      userId = request.user.id
      movie = Movie.objects.filter(uuid=uuid).first()
      listUser = ListContent.objects.filter(user_id=userId).first()
      movieInList = MovieContent.objects.filter(list_content=listUser, movie_id=movie).exists()
     

      if movieInList:
         # Delete
         movie_content = get_object_or_404(MovieContent, movie__uuid=uuid)
         list_content = ListContent.objects.filter(content=movie_content).first()
         movie_content.delete()
      else:
         listUser = ListContent.objects.filter(user_id=userId).first()
         movie_content = MovieContent.objects.create(list_content=listUser, movie=movie)

   if typevideo == 'serie':
      userId = request.user.id
      serie = Serie.objects.filter(uuid=uuid).first()
      listUser = ListContent.objects.filter(user_id=userId).first()
      serieInList = SerieContent.objects.filter(list_content=listUser, serie_id=serie).exists()
     

      if serieInList:
         # Delete
         serie_content = get_object_or_404(SerieContent, serie__uuid=uuid)
         list_content = ListContent.objects.filter(content=serie_content).first()
         serie_content.delete()
      else:
         listUser = ListContent.objects.filter(user_id=userId).first()
         serie_content = SerieContent.objects.create(list_content=listUser, serie=serie)

   return redirect('list')

@login_required(login_url='/login')
def listUser(request):
   listUser = ListContent.objects.filter(user_id=request.user.id).first()
   content = Content.objects.filter(list_content=listUser)

   context = {
      "list": content
   }
   return render(request, 'list.html', context)

@login_required(login_url='/login')
def logout(request):
   # Cerrar sesión
   auth_logout(request)
   return redirect('index')

