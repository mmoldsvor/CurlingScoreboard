from django.db import models
from django.db.models import JSONField


# Create your models here.
class Round(models.Model):
    pos = JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_pos(self):
        return self.pos

    