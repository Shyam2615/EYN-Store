from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home"),
    path('products/<product_category>/', products_page, name="products"),
    path('product/<product_uuid>/', product_page, name="product"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_page, name="logout"),
    path('add-to-cart/<product_uuid>/', add_to_cart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('delete-cart-items/<product_uuid>/', delete_cart_items, name="delete_cart_items"),
    path('checkout/<id>', checkout_page, name="checkout"),
    path('order-placed/', order_placed, name="orderPlaced"),
    path('orders/', orders_page, name="orders_page"),
    path('wishlist/<product_uuid>/', add_wishlist, name="wishlist_page"),
    path('wishlist/', wishlist_page, name="wishlist"),
    path('delete-wishlist/<product_uuid>/', delete_wishlist, name="deleteWishlist"),
]

if settings.DEBUG: 
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)