from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Order, Elements, Hammock_variant
from .forms import VariantsCreateForm

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

class VariantsListView(ListView):
    model = Hammock_variant
    context_object_name = 'variants'

    def post(self, request, *args, **kwargs):
        form = VariantsCreateForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('variants-list')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VariantsCreateForm()
        return context

class VariantsDeleteView(DeleteView):
    model = Hammock_variant
    success_url = '/variants'

class VariantsUpdateView(UpdateView):
    model = Hammock_variant
    success_url = '/variants'
    fields = ['name', 'price']