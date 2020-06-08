from django import forms
from .models import Hammock_variant, Elements, Order

class VariantsCreateForm(forms.ModelForm):
    class Meta:
        model = Hammock_variant
        fields = ['name', 'price']


class OrdersCreateForm(forms.ModelForm):
    class Meta:         
        model = Order
        fields = ['title', 'material', 'client', 'comment', 'postal', 'image']

class NewOrderForm(forms.Form):
    elements_count = forms.IntegerField(max_value=20, min_value=1)
