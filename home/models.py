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
    