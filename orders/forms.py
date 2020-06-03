from django import forms
from .models import Hammock_variant

class VariantsCreateForm(forms.ModelForm):
    class Meta:
        model = Hammock_variant
        fields = ['name', 'price']