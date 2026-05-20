from datetime import datetime

from django.db import models
from Movies.models import Movie
from guests.models import Guest
# Create your models here.

class Reservation(models.Model): 

    reservation_id=models.AutoField(primary_key=True)
    
    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.PROTECT,
        related_name='reservations'
    )

#reserved at: track when the reservation was made
    reserved_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return f"{self.movie.name} at {self.reserved_at} in hall {self.movie.hall_number}"