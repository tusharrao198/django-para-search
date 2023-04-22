import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import timezone
# Create your models here.

class Paragraph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='para_created', default=User, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
class Word(models.Model):
    text = models.CharField(max_length=255, db_index=True)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('text', 'paragraph')

