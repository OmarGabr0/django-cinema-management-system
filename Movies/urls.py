
from django.contrib import admin
from django.urls import include, path
from . import views

app_name='movies'
urlpatterns= [ 
    path('', views.list_movies, name='movies_list'),
    path('list/', views.list_movies, name='movies_list'),
    path('list/<int:id>/', views.list_movie_By_ID, name='movie_by_id'),
    path('edit/<int:id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:id>/', views.delete_movie, name='delete_movie'),
]