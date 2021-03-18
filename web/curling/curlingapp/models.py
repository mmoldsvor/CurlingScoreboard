from django.db import models
from django.db.models import JSONField
import json


# Create your models here.

class Round(models.Model):
    pos = JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    end = models.IntegerField()
    throw = models.IntegerField()
    match = models.CharField(max_length=120)

    def get_pos(self):
        return json.dumps(self.pos) 

class Scoreboard(models.Model):
    winner = models.CharField(max_length=1)
    end = models.IntegerField()
    points = models.IntegerField()
    match = models.CharField(max_length=120)

    def get_score(self):
        return self.end, self.winner, self.points





    