from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum

# Create your models here.

class BaseModel(models.Model):
    product_uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        #In order to make it inheritable

class sizes(BaseModel):
    size = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.size

class products(BaseModel):
    product_category = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to="products", null=True, blank=True)
    product_image1 = models.ImageField(upload_to="products", null=True, blank=True)
    product_image2 = models.ImageField(upload_to="products", null=True, blank=True)
    product_name = models.CharField(max_length=100)
    real_price = models.IntegerField(default=1)
    discounted_price = models.IntegerField(default=1)
    product_description = models.TextField()
    size = models.CharField(max_length=100, default="medium")

    def __str__(self):
        return self.product_name
    

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, related_name="cart")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_cart_total(self):
        return cart_items.objects.filter(cart = self).aggregate(Sum('product__discounted_price'))
    
class cart_items(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartItems")
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    size = models.ForeignKey(sizes, on_delete=models.CASCADE,  null=True, blank=True)

    def __str__(self):
        return self.cart.user.username

class checkout(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.IntegerField()
    Address = models.TextField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, related_name="c_out")
    method = models.CharField(max_length=100, default="COD")
    pincode = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return self.name
    
class wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, related_name="wishlist")
    product = models.ForeignKey(products, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username