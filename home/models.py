from django.db import models

# Create your models here.

class Modified(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class Room(Modified):
    name = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField()
    
    def __str__(self):
        return self.name


class Reservation(Modified):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.room.name} {self.date}"
    
    class Meta:
        unique_together = ('date', 'room',)
        
        