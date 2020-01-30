from django.contrib import admin
from .models import Toppings, Subs, Pasta, Salads, Platters

# Register your models here.
admin.site.register(Toppings)
admin.site.register(Subs)
admin.site.register(Pasta)
admin.site.register(Salads)
admin.site.register(Platters)
