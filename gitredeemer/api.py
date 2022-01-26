from django.urls import path, include

urlpatterns = [
    # path('account/', include('account.api')),
    path('api-auth/', include('rest_framework.urls')),
]
