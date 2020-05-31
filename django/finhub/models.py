from django.db import models

# Create your models here.
class Exchange(models.Model):
    code = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    description = models.CharField(max_length=200)
    displaySymbol = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    def __str__(self):
        return self.description