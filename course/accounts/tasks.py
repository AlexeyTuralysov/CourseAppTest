import requests
from django.conf import settings
from .models import Currency


def update_currency_rates():
    # URL API Fixer.io (замените 'YOUR_ACCESS_KEY' на ваш реальный ключ)
    url = f"http://data.fixer.io/api/latest?access_key={settings.FIXER_API_KEY}&symbols=USD,EUR,GBP"  # Укажите нужные валюты

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data['success']:
            rates = data['rates']
            for currency in Currency.objects.all():
                if currency.name in rates:
                    # Обновляем курс валюты в базе данных
                    currency.course = rates[currency.name]
                    currency.save()
                    print(f"Updated {currency.name} to {currency.course}")
        else:
            print("Error in response data:", data['error'])
    else:
        print("Failed to fetch data from Fixer.io:", response.status_code)