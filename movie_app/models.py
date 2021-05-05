from django.db import models
import uuid

# Create your models here.


class Collection(models.Model):
    user = models.CharField(max_length=50)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=250, null=True)
    movies = models.JSONField()
