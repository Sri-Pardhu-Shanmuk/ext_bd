from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Transactions(models.Model):
    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='transactions'
    )
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.FloatField()
    type = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}-{self.title} - {self.amount}"

    