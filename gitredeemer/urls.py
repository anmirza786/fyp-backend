from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
# from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    path('api/', include('gitredeemer.api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += [
#     re_path(r'^.*', TemplateView.as_view(template_name='index.html'))
# ]
