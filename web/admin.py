from django.contrib import admin
from .models import Product, Compare, Wishlist, Order, OrderItem
# Register your models here.
class OrderItemTuble(admin.TabularInline):
    model = OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTuble]
admin.site.register(Product)
admin.site.register(Compare)
admin.site.register(Wishlist)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
