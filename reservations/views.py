from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Core Imports for CBVs, Mixins, and Generics
from rest_framework.views import APIView
from rest_framework import generics, mixins

from reservations.models import Reservation
from Movies.models import Movie
from guests.models import Guest
from .serializers import ReservationSerializer

####### WEB UI (FBV) ######

def list_reservations(request):
    # Optimization: pre-fetching foreign keys in a single query
    reservations_list = Reservation.objects.all().select_related('guest', 'movie')
    return render(
        request, 
        'reservations/reservations_list.html', 
        {'reservations': reservations_list}
    )


def book_reservation(request):
    if request.method == 'POST':
        guest_id = request.POST['guest']
        movie_id = request.POST['movie']
        
        guest = get_object_or_404(Guest, pk=guest_id)
        movie = get_object_or_404(Movie, pk=movie_id)
        
        Reservation.objects.create(
            guest=guest,
            movie=movie
        )
        return redirect('reservations:reservations_list')
        
    # GET request: load available options for form dropdown selection selectors
    guests = Guest.objects.all()
    movies = Movie.objects.all()
    return render(
        request, 
        'reservations/booking_form.html', 
        {'guests': guests, 'movies': movies}
    )


def cancel_reservation(request, id):
    reservation = get_object_or_404(Reservation, pk=id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations:reservations_list')
    return render(
        request, 
        'reservations/cancel_reservation.html', 
        {'reservation': reservation}
    )


##### API Views Layer #####

#api/v1: FBV
@api_view(['GET', 'POST'])
def reservation_api_list(request):
    if request.method == 'GET':
        reservations = Reservation.objects.all().select_related('guest', 'movie')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def reservation_api_detail(request, id):
    reservation = get_object_or_404(Reservation, pk=id)
    
    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
        
    elif request.method == 'DELETE':
        reservation.delete()
        return Response(
            {'message': 'Reservation cancelled successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )


#api/v2: CBV
class ReservationListCBV(APIView):
    def get(self, request):
        reservations = Reservation.objects.all().select_related('guest', 'movie')
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetailCBV(APIView):
    def get(self, request, id):
        reservation = get_object_or_404(Reservation, pk=id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def delete(self, request, id):
        reservation = get_object_or_404(Reservation, pk=id)
        reservation.delete()
        return Response(
            {'message': 'Reservation cancelled successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )


#api/v3: Mixins
class ReservationListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Reservation.objects.all().select_related('guest', 'movie')
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReservationDetailMixins(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#api/v4: Generic Views
class ReservationListGenerics(generics.ListCreateAPIView):
    queryset = Reservation.objects.all().select_related('guest', 'movie')
    serializer_class = ReservationSerializer


class ReservationDetailGenerics(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'