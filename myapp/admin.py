from django.contrib import admin
from .models import Categories,Product,Cart,Tracking,Payment,SellerProduct


class SellerProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'price', 'approval_status')  # Display the status in the admin panel
    list_filter = ('approval_status',)  # Add a filter to easily find pending, approved, or rejected products
    search_fields = ('name', 'user__username')  # Make it searchable by product name and seller username


# Register your models here.
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Tracking)
admin.site.register(Payment)
admin.site.register(SellerProduct,SellerProductAdmin)