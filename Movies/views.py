from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from Movies.models import Movie
from Movies.serializers import MovieSerializer


####### WEB UI (FBV) ######

def list_movies(request):

    movies_list = Movie.objects.all()

    return render(
        request,
        'movies/movies_list.html',
        {'movies': movies_list}
    )


def list_movie_By_ID(request, id):

    movie = get_object_or_404(Movie, pk=id)

    return render(
        request,
        'movies/movie_by_id.html',
        {'movie': movie}
    )


def add_movie(request):

    if request.method == 'POST':

        # Convert duration string to timedelta
        duration_str = request.POST['duration']

        hours, minutes, seconds = map(int, duration_str.split(':'))

        duration = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )

        Movie.objects.create(
            name=request.POST['name'],
            start_time=request.POST['start_time'],
            duration=duration,
            hall_number=request.POST['hall_number'],
            reservation_price=request.POST['reservation_price']
        )

        return redirect('movies:movies_list')

    return render(request, 'movies/add_movie.html')


def edit_movie(request, id):

    movie = get_object_or_404(Movie, pk=id)

    if request.method == 'POST':

        # Convert duration string to timedelta
        duration_str = request.POST['duration']

        hours, minutes, seconds = map(int, duration_str.split(':'))

        duration = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )

        movie.name = request.POST['name']
        movie.start_time = request.POST['start_time']
        movie.duration = duration
        movie.hall_number = request.POST['hall_number']
        movie.reservation_price = request.POST['reservation_price']

        movie.save()

        return redirect('movies:movies_list')

    return render(
        request,
        'movies/edit_movie.html',
        {'movie': movie}
    )


def delete_movie(request, id):

    movie = get_object_or_404(Movie, pk=id)

    if request.method == 'POST':

        movie.delete()

        return redirect('movies:movies_list')

    return render(
        request,
        'movies/delete_movie.html',
        {'movie': movie}
    )


##### API Views Layer #####

#api/v1: FBV
@api_view(['GET', 'POST'])
def movie_api_list(request):

    if request.method == 'GET':

        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def movie_api_detail(request, id):

    movie = get_object_or_404(Movie, pk=id)

    if request.method == 'GET':

        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        movie.delete()

        return Response(
            {'message': 'Movie deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


#api/v2: CBV
class MovieListCBV(APIView):

    def get(self, request):

        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MovieDetailCBV(APIView):

    def get(self, request, id):

        movie = get_object_or_404(Movie, pk=id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    def put(self, request, id):

        movie = get_object_or_404(Movie, pk=id)

        serializer = MovieSerializer(movie, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):

        movie = get_object_or_404(Movie, pk=id)

        movie.delete()

        return Response(
            {'message': 'Movie deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


#api/v3: Mixins
class MovieListMixins(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)


class MovieDetailMixins(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'movie_id'

    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)


#api/v4: Generic Views
class MovieListGeneric(ListCreateAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailGeneric(RetrieveUpdateDestroyAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'movie_id'