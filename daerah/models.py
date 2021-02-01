from django.db import models


class Daerah(models.Model):
    kode = models.CharField(max_length=13)
    nama = models.CharField(max_length=255)
