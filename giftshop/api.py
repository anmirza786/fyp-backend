from django.urls import path, include
from giftshop import views

urlpatterns = [
    # path('account/', include('account.api')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('competitions/', include('competitions.api')),
    # path('gift-shop/', include('giftshop.api')),
    path('', views.GiftShopApiView.as_view()),
    path('<pk>', views.GiftApiView.as_view())
]
