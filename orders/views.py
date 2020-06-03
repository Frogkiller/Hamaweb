from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, reverse
from django.forms import inlineformset_factory
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from .models import Order, Elements, Hammock_variant, Client
from .forms import VariantsCreateForm, ElementForm
import logging

logger = logging.getLogger(__name__)

class OrdersListView(ListView):
    model = Order
    template_name = 'orders/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'orders'
    ordering = ['-date_created']

class OrdersCreateView(CreateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image']
    # new_f = []
    
    def get_context_data(self, **kwargs):
        context = super(OrdersCreateView, self).get_context_data(**kwargs)
        if self.kwargs.get('magic'):
            value = self.kwargs.get('magic')
        else:
            value = 0
        ElementsInlineFormSet = inlineformset_factory(Order, Elements, fields=('variant', 'count', 'price_override'), extra=value)
        context['ham_variants'] = Hammock_variant.objects.all()
        if self.request.POST:
            context['formset'] = ElementsInlineFormSet(self.request.POST)
        else:
            context['formset'] = ElementsInlineFormSet()
        # pk = self.kwargs.get('magic')
        # if pk:
        #     ham = get_object_or_404(Hammock_variant, id=pk)
        #     ele = Elements(variant=ham, price_override=ham.price)
        #     form = ElementForm(instance=ele)
        #     self.new_f.append(form)
        #     context['cur_var'] = self.new_f
        # else:
        #     self.new_f = []
        return context
    # def post(self, request, *args, **kwargs):

    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        f2 = context['formset']
        if f2.is_valid():
            self.object = form.save()
            f2.instance = self.object
            f2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrdersDetailView(DetailView):
    model = Order

class OrdersDeleteView(DeleteView):
    model = Order
    success_url = '/'

class OrdersUpdateView(UpdateView):
    model = Order
    fields = ['title', 'material', 'client', 'comment', 'postal', 'image']

    def get_context_data(self, **kwargs):
        context = super(OrdersUpdateView, self).get_context_data(**kwargs)
        ElementsInlineFormSet = inlineformset_factory(Order, Elements, fields=('variant', 'count', 'price_override'), extra=0)
        if self.request.POST:
            context['formset'] = ElementsInlineFormSet(self.request.POST, instance=self.get_object())
        else:
            context['formset'] = ElementsInlineFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        f2 = context['formset']
        if f2.is_valid():
            self.object = form.save()
            f2.instance = self.object
            f2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))



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