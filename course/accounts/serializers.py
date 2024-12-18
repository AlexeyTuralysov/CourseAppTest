from rest_framework import serializers
from .models import Currency,CurrencyFavorite




class CurrencySerizliazer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'course','code']


class CurrencyFavoriteSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code')  # Добавляем код валюты

    class Meta:
        model = CurrencyFavorite
        fields = ['id', 'currency_code']
