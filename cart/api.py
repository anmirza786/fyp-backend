from django.urls import path
from . import views

urlpatterns = [
    # path("", views.ActiveCartApiView.as_view()),
    path("active/", views.ActiveCartApiView.as_view()),
    path("order/", views.OrderApiView.as_view()),
    path("add/", views.CartItemCreateApiView.as_view()),
    path("delete/<int:pk>", views.CartItemDeleteApiView.as_view()),
]