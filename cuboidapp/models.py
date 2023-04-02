from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boxes_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def area(self):
    #     return self.length * self.breadth

    # def volume(self):
    #     return self.length * self.breadth * self.height


