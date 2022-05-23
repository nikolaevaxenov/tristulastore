from django.contrib import admin
from .models import Product, Order, Order_Product, Feedback, Event


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_Product)
admin.site.register(Feedback)
admin.site.register(Event)
