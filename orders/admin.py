from django.contrib import admin
from .models import Client, Hammock_variant, Order, Elements

admin.site.register(Client)
admin.site.register(Hammock_variant)
admin.site.register(Order)
admin.site.register(Elements)
