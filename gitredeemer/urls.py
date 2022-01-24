from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('api/', include('gitredeemer.api')),
    # path('api/token/', TokenObtainPairView.as_view()),
    # path('api/token/refresh/', TokenRefreshView.as_view()),
    # path('api/token/verify/', TokenVerifyView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
