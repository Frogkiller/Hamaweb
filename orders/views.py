from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Order, Elements


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'
    ordering = ['-date_created']

class OrdersCreateView(CreateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image', 'variants']

class OrdersDetailView(DetailView):
    model = Order

class OrdersDeleteView(DeleteView):
    model = Order
    success_url = '/'

class OrdersUpdateView(UpdateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image', 'variants' ]