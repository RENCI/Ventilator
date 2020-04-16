from django.db import models

class Pressure(models.Model):
    id =  models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length = 50)
    value = models.FloatField()
    ts = models.DateTimeField(null = True)

class Respiration(models.Model):
    id =  models.AutoField(primary_key=True)
    value = models.FloatField()
    ts = models.DateTimeField(null = True)

class Configuration(models.Model):
    id =  models.AutoField(primary_key=True)
    param_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.CharField(max_length = 50)
    ts = models.DateTimeField(null=True)

class Calibration(models.Model):
    id =  models.AutoField(primary_key=True)
    param_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.CharField(max_length = 50)
    ts = models.DateTimeField(null=True)

class Diagnostic(models.Model):
    id =  models.AutoField(primary_key=True)
    test_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    result = models.FloatField()
    grouping = models.IntegerField()
    ts = models.DateTimeField(null=True)