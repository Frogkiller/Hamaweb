from django.urls import path
from .views import (
    OrdersListView,
    OrdersCreateView,
    OrdersDetailView,
    OrdersDeleteView,
    OrdersUpdateView,
    VariantsListView,
    VariantsUpdateView,
    VariantsDeleteView,
    ClientsListView,
    ClientsUpdateView,
    ClientsDeleteView,
    ClientsCreateView,
)

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders-home'),
    path('order/new', OrdersCreateView.as_view(), name='orders-create'),
    path('order/<int:pk>', OrdersDetailView.as_view(), name='orders-detail'),
    path('order/update/<int:pk>', OrdersUpdateView.as_view(), name='orders-update'),
    path('order/delete/<int:pk>', OrdersDeleteView.as_view(), name='orders-delete'),
    path('order/<int:pk>', OrdersDetailView.as_view(), name='orders-detail'),
    path('variants/', VariantsListView.as_view(), name='variants-list'),
    path('variants/update/<int:pk>', VariantsUpdateView.as_view(), name='variants-update'),
    path('variants/delete/<int:pk>', VariantsDeleteView.as_view(), name='variants-delete'),
    path('clients/', ClientsListView.as_view(), name='clients-list'),
    path('clients/new', ClientsCreateView.as_view(), name='clients-create'),
    path('clients/update/<int:pk>', ClientsUpdateView.as_view(), name='clients-update'),
    path('clients/<int:pk>', ClientsDeleteView.as_view(), name='clients-delete'),
]
