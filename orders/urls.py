from django.urls import path
from .views import (
    OrdersListView
)

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-home')
]
