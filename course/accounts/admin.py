from django.contrib import admin
from .models import Profile,Currency,CurrencyFavorite
# Register your models here.

admin.site.register(Profile)
admin.site.register(Currency)
admin.site.register(CurrencyFavorite)