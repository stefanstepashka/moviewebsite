
from django.contrib import admin
from django.urls import path
from movie_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('movies/', views.show_all_movies),
    path('movies/<int:id_mov>', views.one_movie, name='one_movie'),
    path('directors/', views.all_directors),
    path('directors/<int:id_dir>', views.one_director, name='one_director'),
    path('actors/', views.all_actors),
    path('actors/<int:id_act>', views.one_actor, name='one_actors')
]
