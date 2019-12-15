from django.db import models


class Profiles(models.Model):
    first_name = models.CharField(max_length=450)
    last_name = models.CharField(max_length=450)
    username = models.CharField(max_length=450)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    referral = models.ManyToManyField('Profiles')
