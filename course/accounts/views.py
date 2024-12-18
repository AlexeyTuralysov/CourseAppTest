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


    url = f"http://data.fixer.io/api/latest?access_key=503e97796596f0a9ca139e1d449035bf&base=EUR&symbols={symbols}"


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

        url = f"http://data.fixer.io/api/latest?access_key=503e97796596f0a9ca139e1d449035bf&base=EUR&symbols={symbols}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['success']:
                rates = data['rates']
                updated_currencies = []

                for currency in Currency.objects.all():
                    if currency.name in rates:
                        currency.course = rates[currency.name]
                        currency.save()
                        updated_currencies.append(CurrencySerizliazer(currency).data)

                return Response(updated_currencies, status=status.HTTP_200_OK)
            else:
                return Response({"ошибка": data['error']}, status=status.HTTP_400_BAD_REQUEST)