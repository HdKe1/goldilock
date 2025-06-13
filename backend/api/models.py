from django.db import models

# Create your models here.

class Stats(models.Model):
    username = models.CharField(max_length=100)
    avg_wpm = models.FloatField(default = 0.0,null = True,blank = True)
    last_wpm = models.FloatField(default = 0.0,null = True,blank = True)
