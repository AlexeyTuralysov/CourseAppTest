from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    profile_owner = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.profile_owner.username


class Currency(models.Model):
    name = models.CharField(max_length=50)
    course = models.DecimalField(max_digits=10, decimal_places=4)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.course} в евро)"


class CurrencyFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)



    class Meta:
        unique_together = ('user', 'currency')

    def __str__(self):
        return f"{self.user.username} в избранном {self.currency.name}"