from django.urls import path, include
from giftshop import views

urlpatterns = [
    # path('profile/', include('account.api')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('competitions/', include('competitions.api')),
    # path('gift-shop/', include('giftshop.api')),
    path('gift-shop/', views.GiftShopApiView.as_view()),
    path('ecard/', views.EcardApiView.as_view()),
]
