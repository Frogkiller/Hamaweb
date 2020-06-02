from django.urls import path
from .views import (
    OrdersListView,
    OrdersCreateView,
    OrdersDetailView,
    OrdersDeleteView,
    OrdersUpdateView,
)

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-home'),
    path('order/new', OrdersCreateView.as_view(), name='orders-create'),
    path('order/<int:pk>', OrdersDetailView.as_view(), name='orders-detail'),
    path('order/update/<int:pk>', OrdersUpdateView.as_view(), name='orders-update'),
    path('order/delete/<int:pk>', OrdersDeleteView.as_view(), name='orders-delete'),
    path('order/<int:pk>', OrdersDetailView.as_view(), name='orders-detail'),
]
