
from django.db import models

# Create your models here.
class Movie(models.Model): 
    movie_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    start_time=models.DateTimeField()
    duration=models.DurationField()
    hall_number=models.IntegerField()
    reservation_price=models.DecimalField(max_digits=5, decimal_places=2)
   
    def __str__(self): 
        return f"{self.name}: {self.duration} - {self.reservation_price}"