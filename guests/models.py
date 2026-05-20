from django.db import models

# Create your models here.
class Guest(models.Model):
    guest_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    #phone_number=models.CharField(max_length=20, blank=True, null=True)

    def __str__(self): 
        return f"{self.name} - {self.email}"
    