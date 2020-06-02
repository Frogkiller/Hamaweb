from django.shortcuts import render
from django.views.generic import (
    ListView,
)
from .models import Order, Elements


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'
    ordering = ['-date_created']


