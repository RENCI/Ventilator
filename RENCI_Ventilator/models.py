from django.db import models

class pressure(models.Model):
    id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    value = models.FloatField()

class repiration(models.Model):
    id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    value = models.FloatField()

class configuration(models.Model):
    id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.FloatField()

