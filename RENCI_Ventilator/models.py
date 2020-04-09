from django.db import models

class pressure(models.Model):
    id =  models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length = 50)
    value = models.FloatField()
    ts = models.DateTimeField(null = True)

class repiration_rate(models.Model):
    id =  models.AutoField(primary_key=True)
    value = models.FloatField()
    ts = models.DateTimeField(null = True)

class configuration(models.Model):
    id =  models.AutoField(primary_key=True)
    param_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.FloatField()
    ts = models.DateTimeField(null=True)

class calibration(models.Model):
    id =  models.AutoField(primary_key=True)
    param_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.FloatField()
    ts = models.DateTimeField(null=True)

class diagnostics(models.Model):
    id =  models.AutoField(primary_key=True)
    param_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    value = models.FloatField()
    ts = models.DateTimeField(null=True)