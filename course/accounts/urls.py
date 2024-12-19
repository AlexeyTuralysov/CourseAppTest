from django.contrib import admin
from django.urls import path, include
from .views import index,UpdateCurrencyRatesView,addtofavoryte,getFavoriteBySymbols,deleteFromFavorite,PreviousDayCurrencyRatesView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", index ,name="index"),
    path("course-add/", addtofavoryte ,name="add_favoryte"),

    path('currency-rates/', UpdateCurrencyRatesView.as_view(), name='update_currency_rates'),

    path('currency-rates-previous/', PreviousDayCurrencyRatesView.as_view(), name='currency-rates-previous'),

    path('getfavoritebysymbols/', getFavoriteBySymbols, name='getFavoriteBySymbols'),

    path('api/removeFavorite/<str:currency_code>/', deleteFromFavorite, name='delete_favorite_currency'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]