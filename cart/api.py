from django.urls import path
from . import views

urlpatterns = [
    path("", views.ActiveCartApiView.as_view()),
    path("cart-item/<int:pk>/", views.RetriveOrderitemsApiView.as_view()),
]