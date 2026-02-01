# admin.py

from django.contrib import admin
from .models.models import Post
from .models.customer import Customer
from .models.category import Category
from .models.product import Products, ProductImage
from .models.comment import Comment
from .models.shippingaddress import Order 

from .views.store import send_order_status_email

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'formatted_price', 'category']  # Use formatted_price instead of price

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'shipping_cost', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_address__city']

    def save_model(self, request, obj, form, change):
        if change:
            original = Order.objects.get(pk=obj.pk)
            if original.status != obj.status:
                # Gửi email nếu status thay đổi
                if obj.shipping_address and obj.shipping_address.email:
                    send_order_status_email(
                        email=obj.shipping_address.email,
                        order=obj
                    )
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Post)
admin.site.register(Customer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, AdminProduct)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Order, OrderAdmin) 