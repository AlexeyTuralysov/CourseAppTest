from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from .serializers import CurrencySerizliazer,CurrencyFavoriteSerializer
from .models import Currency,CurrencyFavorite

tokenFixer = "a2d6c43c59df0832561c96f7cde8f29c"

# Create your views here.
def index(request):
    return HttpResponse("200+")




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFavoriteBySymbols(req):
    user = req.user
    favorites = CurrencyFavorite.objects.filter(user=user)

    if not favorites.exists():
        return Response({"message": "У вас нет избранных валют."}, status=status.HTTP_404_NOT_FOUND)


    symbols = ','.join([favorite.currency.code for favorite in favorites])


    url = f"http://data.fixer.io/api/latest?access_key={tokenFixer}&base=EUR&symbols={symbols}"


    response = requests.get(url)

    if response.status_code != 200:
        return Response({"error": "Ошибка получения данных с Fixer.io."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = response.json()


    if 'error' in data:
        return Response({"error": data['error']['info']}, status=status.HTTP_400_BAD_REQUEST)


    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def addtofavoryte(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_403_FORBIDDEN)

    data = request.data


    if 'currency' not in data:
        return Response({"error": "Currency is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:

        curr= Currency.objects.get(code=data['currency'])

    except Currency.DoesNotExist:
        return Response({"error": "Currency not found."}, status=status.HTTP_404_NOT_FOUND)


    note, created = CurrencyFavorite.objects.get_or_create(
        user=request.user,
        currency=curr
    )



    ser = CurrencyFavoriteSerializer(note)
    return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def deleteFromFavorite(request, currency_code):
    try:

        user = request.user
        favorite_currency = CurrencyFavorite.objects.get(user=user, currency__code=currency_code)


        favorite_currency.delete()

        return Response({"message": "Dалюта  удалена из избранного."}, status=status.HTTP_204_NO_CONTENT)

    except CurrencyFavorite.DoesNotExist:
        return Response({"error": "валюта не найдена в избранном."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCurrencyRatesView(APIView):
    def get(self, request):
        cur = Currency.objects.values_list('code', flat=True)
        symbols = ','.join(cur)

        # Получение текущих курсов
        url_current = f"http://data.fixer.io/api/latest?access_key={tokenFixer}&base=EUR&symbols={symbols}"
        response_current = requests.get(url_current)

        # Получение курсов за предыдущий день
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url_previous = f"http://data.fixer.io/api/{yesterday}?access_key={tokenFixer}&base=EUR&symbols={symbols}"
        response_previous = requests.get(url_previous)

        if response_current.status_code == 200 and response_previous.status_code == 200:
            data_current = response_current.json()
            data_previous = response_previous.json()

            if data_current['success'] and data_previous['success']:
                rates_current = data_current['rates']
                rates_previous = data_previous['rates']
                updated_currencies = []

                for currency in Currency.objects.all():
                    if currency.name in rates_current and currency.name in rates_previous:
                        currency.course = rates_current[currency.name]
                        currency.save()
                        updated_currencies.append({
                            "code": currency.name,
                            "course": rates_current[currency.name],
                            "previous_course": rates_previous[currency.name]
                        })

                return Response(updated_currencies, status=status.HTTP_200_OK)
            else:
                return Response({"ошибка": data_current.get('error', 'Ошибка данных')},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"ошибка": "Ошибка соединения с Fixer.io"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PreviousDayCurrencyRatesView(APIView):
    def get(self, request):
        tokenFixer = "ВАШ_API_КЛЮЧ"  # Ваш API-ключ для Fixer.io или другого сервиса
        cur = Currency.objects.values_list('code', flat=True)
        symbols = ','.join(cur)

        # Получение даты вчерашнего дня
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Запрос курсов за предыдущий день через API
        url = f"http://data.fixer.io/api/{yesterday}?access_key={tokenFixer}&base=EUR&symbols={symbols}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['success']:
                rates = data['rates']
                previous_currencies = []

                # Сохраняем курсы валют за предыдущий день в список
                for currency in Currency.objects.all():
                    if currency.name in rates:
                        previous_currencies.append({
                            "code": currency.name,
                            "course": rates[currency.name]
                        })

                return Response(previous_currencies, status=status.HTTP_200_OK)
            else:
                return Response({"ошибка": data['error']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"ошибка": "Ошибка соединения с Fixer.io"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)