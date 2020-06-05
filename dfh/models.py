import uuid
from django.db import models

# Create your models here.
class Key(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    p = models.IntegerField()
    g = models.IntegerField()
    a = models.IntegerField()
    key = models.BigIntegerField()
    email = models.EmailField()
