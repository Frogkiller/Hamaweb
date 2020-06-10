from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from django.forms import inlineformset_factory
from django.utils import timezone
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView
)
from .models import Order, Elements, Hammock_variant, Client
from .forms import VariantsCreateForm, NewOrderForm
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class NewOrderFormView(FormView):
    template_name = 'orders/order_new.html'
    form_class = NewOrderForm

    def get_success_url(self):
        form = self.form_class(self.request.POST or None)
        if form.is_valid():
            return reverse('orders-create-get', kwargs={'elements_count': form.data['elements_count']})
        return reverse('order-create')

class OrdersListView(ListView):
    model = Order
    template_name = 'orders/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'
    ordering = ['-date_created']

class OrdersCreateView(CreateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image']
    
    def get_context_data(self, **kwargs):
        context = super(OrdersCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('elements_count'):
            value = self.kwargs.get('elements_count')
        else:
            value = 0
        ElementsInlineFormSet = inlineformset_factory(Order, Elements, fields=('variant', 'count', 'price_override'), extra=value)
        context['ham_variants'] = Hammock_variant.objects.all()
        if self.request.POST:
            context['formset'] = ElementsInlineFormSet(self.request.POST)
        else:
            context['formset'] = ElementsInlineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        f2 = context['formset']
        if f2.is_valid():
            self.object = form.save(commit=False)
            self.object.number_of_elements = sum([int(x['count'].value()) for x in f2 if x['variant'].value() != ''])
            f2.instance = self.object
            formset = f2.save(commit=False)
            for f in formset:
                if f.price_override == Decimal(0):
                    f.price_override = f.variant.price
            self.object.sumaric_price = sum([x.price_override*x.count for x in formset]) + (10 if self.object.postal else 0)
            self.object.save()
            for f in formset: f.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrdersDetailView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrdersDetailView, self).get_context_data(**kwargs)
        context['variants'] = Elements.objects.filter(order=self.object).all()
        context['isnt_completed'] = True if self.object.complete_date is None else False
        return context

class OrdersDeleteView(DeleteView):
    model = Order
    success_url = '/'

class OrdersUpdateView(UpdateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image']

    def get_context_data(self, **kwargs):
        context = super(OrdersUpdateView, self).get_context_data(**kwargs)
        ElementsInlineFormSet = inlineformset_factory(Order, Elements, fields=('variant', 'count', 'price_override'), extra=1)
        if self.request.POST:
            context['formset'] = ElementsInlineFormSet(self.request.POST, instance=self.get_object())
        else:
            context['formset'] = ElementsInlineFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        f2 = context['formset']
        if f2.is_valid():
            self.object = form.save(commit=False)
            self.object.number_of_elements = sum([int(x['count'].value()) for x in f2 if x['variant'].value() != ''])
            self.object.sumaric_price = sum([float(x['price_override'].value())*float(x['count'].value()) for x in f2]) + (10 if self.object.postal else 0) 
            self.object.save()
            f2.instance = self.object
            f2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

def OrdersComplete(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    obj.complete_date = timezone.now()
    obj.save()
    messages.success(request, f'This order has been completed')
    return redirect('orders-detail', pk=pk)


class VariantsListView(ListView):
    model = Hammock_variant
    context_object_name = 'variants'

    def post(self, request, *args, **kwargs):
        form = VariantsCreateForm(self.request.POST or None)
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

class ClientsListView(ListView):
    model = Client
    context_object_name = 'clients'
    ordering = ['-date_added']

class ClientsDeleteView(DeleteView):
    model = Client
    success_url = '/clients'

class ClientsUpdateView(UpdateView):
    model = Client
    success_url = '/clients'
    fields = ['name', 'phone', 'inpost', 'comments']

class ClientsCreateView(CreateView):
    model = Client
    success_url = '/clients'
    fields = ['name', 'phone', 'inpost', 'comments']