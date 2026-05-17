from rest_framework import serializers
from reservations.models import Reservation
from guests.serializers import GuestSerializer
from Movies.serializers import MovieSerializer # Assuming you have this serializer

class ReservationSerializer(serializers.ModelSerializer):
    # Read-only nested serialization for listing/retrieving data
    guest_details = GuestSerializer(source='guest', read_only=True)
    movie_details = MovieSerializer(source='movie', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'reservation_id', 
            'guest', 
            'movie', 
            'reserved_at', 
            'guest_details', 
            'movie_details'
        ]
        
        extra_kwargs = {
            'guest': {'write_only': True},
            'movie': {'write_only': True}
        }