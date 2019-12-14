from django.db import models


class Button(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Text(models.Model):
    button = models.ForeignKey('Button', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text
