from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework import routers
from .api import MoviesViewSet, SeriesViewSet

router = routers.DefaultRouter()
router.register(r'movies', MoviesViewSet, 'movie')

router.register(r'series', SeriesViewSet, 'serie')



urlpatterns = [
    path('', views.index, name='index'),
    path('movies', views.movies, name='movies'),
    path('movie/<str:movie_uuid>', views.movie, name='movie'),
    path('series', views.series, name='series'),
    path('serie/<str:serie_uuid>', views.serie, name='serie'),
    path('chapter/<str:chapter_uuid>', views.chapter, name='chapter'),
    path('login', views.login, name='login'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('logout', views.logout, name='logout'),
    path('toggle-to-list/<str:typevideo>/<str:uuid>', views.toggleToList, name='toggleToList'),
    path('list', views.listUser, name='list'),

    path('api/', include(router.urls)),
]

