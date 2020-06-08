from django import forms
from .models import Hammock_variant, Elements, Order

class VariantsCreateForm(forms.ModelForm):
    class Meta:
        model = Hammock_variant
        fields = ['name', 'price']


class ElementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(ElementForm, self).__init__(*args, **kwargs) 
    #    self.fields['variant'].disabled = True 

    class Meta:         
        model = Elements
        fields = ['variant', 'count', 'price_override']


class OrdersCreateForm(forms.ModelForm):
    class Meta:         
        model = Order
        fields = ['title', 'material', 'client', 'comment', 'postal', 'image']

class NewOrderForm(forms.Form):
    elements_count = forms.IntegerField(max_value=20, min_value=1)
