from django.urls import path, include

urlpatterns = [
    # path('account/', include('account.api')),
    path('api-auth/', include('rest_framework.urls')),
    path('competitions/', include('competitions.api')),
    path('gift-shop/', include('giftshop.api')),
    path('carts/', include('cart.api')),
]
