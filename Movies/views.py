from urllib import request

from django.shortcuts import get_object_or_404, redirect, render
from Movies.models import *

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from Movies.serializers import MovieSerializer

# Create your views here.

#FPV 
def list_movies(request):

    movies_list=Movie.objects.all()
    return render(request, 'movies/movies_list.html',{'movies': movies_list})

def list_movie_By_ID(request, id):
    movie=Movie.objects.get(movie_id=id)
    return render(request, 'movies/movie_by_id.html',{'movie': movie})

def edit_movie(request, id):

    movie = get_object_or_404(Movie, pk=id)

    if request.method == 'POST':

        movie.name = request.POST['name']
        movie.hall_number = request.POST['hall_number']
        movie.reservation_price = request.POST['reservation_price']
        movie.duration = request.POST['duration']
        movie.save()

        return redirect('movies:movies_list')

    return render(request, 'Movies/edit_movie.html', {'movie': movie})
def delete_movie(request, id):
    movie=get_object_or_404(Movie, pk=id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movies_list')
    return render(request, 'Movies/delete_movie.html', {'movie': movie})



class MovieListGeneric(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailGeneric(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'movie_id'