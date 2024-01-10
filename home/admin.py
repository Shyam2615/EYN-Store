from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(products)
admin.site.register(Cart)
admin.site.register(cart_items)
admin.site.register(checkout)
admin.site.register(wishlist)
admin.site.register(sizes)