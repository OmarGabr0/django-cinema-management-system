from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = [
            'movie_id',
            'name',
            'start_time',
            'duration',
            'hall_number',
            'reservation_price',
        ]