from django import forms
from .models import Hammock_variant, Elements, Order, Balance

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


class BalanceCreateForm(forms.ModelForm):
    count = forms.DecimalField(max_value=5, decimal_places=1, min_value=0)
    price = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0)
    class Meta:
        model = Balance
        fields = ['title']
