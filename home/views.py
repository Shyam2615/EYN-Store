from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.core.paginator import Paginator
from random import sample


# Create your views here.

@login_required(login_url='/login/')
def home_page(request):
    user = request.user
    product = products.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        product = product.filter(
            Q(product_name__icontains = search) |
            Q(product_category__icontains = search)
        )
    items = products.objects.all()
    # items = sample(list(items), min(8, len(items)))
    items = items[:8]
    mens_Winter_Wear = products.objects.filter(product_category = "Mens Winter Wear")
    mens_Winter_Wear = sample(list(mens_Winter_Wear), min(4, len(mens_Winter_Wear)))
    # mens_Winter_Wear = mens_Winter_Wear[:4]
    electronics = products.objects.filter(product_category = "Electronics")
    electronics = sample(list(electronics), min(4, len(electronics)))
    length = len(cart_items.objects.filter(cart__user = user, cart__is_paid = False))
    w_length = len(wishlist.objects.filter(user=user))
    searched = False
    if request.GET.get('search'):
        searched = True
        paginator = Paginator(product, 4)  # Show 25 contacts per page.
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context={"products":page_obj, "search":search, "searched":searched , "items":items, "mens":mens_Winter_Wear, "length":length,"w_length":w_length}
    else:
        context={"items":items, "mens":mens_Winter_Wear, "electronics":electronics, "length":length,"w_length":w_length}
    return render(request, 'home.html', context)

@login_required(login_url='/login/')
def products_page(request, product_category):
    user = request.user
    product = products.objects.filter(product_category = product_category)
    paginator = Paginator(product, 10)  # Show 25 contacts per page.

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"products":page_obj}
    search_result = products.objects.all()
    searched = False
    if request.GET.get('search'):
       search = request.GET.get('search')
       searched = True
       search_result = search_result.filter(
           Q(product_name__icontains = search) |
           Q(product_category__icontains = search)
       )
       paginator = Paginator(search_result, 10)  # Show 25 contacts per page.

       page_number = request.GET.get("page", 1)
       page_obj = paginator.get_page(page_number)
       context["searched"] = searched
       context["results"] = page_obj
    length = len(cart_items.objects.filter(cart__user = user, cart__is_paid = False))
    w_length = len(wishlist.objects.filter(user=user))
    context["length"]=length
    context["w_length"] = w_length
    return render(request, "products.html",context=context)

@login_required(login_url='/login/')
def product_page(request, product_uuid):
    user = request.user
    items = products.objects.get(product_uuid = product_uuid)
    category = items.product_category
    similar = products.objects.filter(product_category = category)
    similar = sample(list(similar), min(8, len(similar)))
    length = len(cart_items.objects.filter(cart__user = user, cart__is_paid = False))
    w_length = len(wishlist.objects.filter(user=user))
    size = sizes.objects.all()
    context = {"item":items}
    # context['item']=items
    product = products.objects.all()
    searched = False
    if request.GET.get('search'):
        search = request.GET.get('search')
        product = product.filter(
            Q(product_name__icontains = search) |
            Q(product_category__icontains = search)
        )
        searched = True
        paginator = Paginator(product, 8)  # Show 25 contacts per page.
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context['search'] = search
        context['searched'] = searched
        context['products'] = page_obj
    context['similars']=similar
    context['length']=length
    context['w_length']=w_length
    context['sizes']=size
    if request.GET.get('size'):
        Size = request.GET.get('size')
        print(Size)
        context['selected_size'] = Size
    # context = {"item": items,"similars":similar, "length":length,"w_length":w_length,"sizes":size,}
    
    return render(request, "product.html", context = context)

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "User already exists")
            return redirect('/register')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully")
        return redirect('/')

    return render(request, "register.html")

def login_page(request):
    if request.method == "POST":
       username = request.POST.get('username')
       password = request.POST.get('password')

       if not User.objects.filter(username = username):
           messages.info(request, "Enter the correct username")
           return redirect("/login")
       
       user = authenticate(username=username, password=password)

       if user is None:
           messages.info(request, "Enter the correct password")
           return redirect('/login')
       else:
           login(request, user)
           return redirect('/')
       
    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect('/login')

def add_to_cart(request, product_uuid,):
    user = request.user
    item = products.objects.get(product_uuid = product_uuid)
    cart, _ = Cart.objects.get_or_create(
        user = user,
        is_paid = False
    )

    if request.GET.get('size'):
        size = request.GET.get('size')
        Size = sizes.objects.get(size=size)
        cart_items.objects.create(
            cart = cart,
            product = item,
            size = Size
        )
    else:
        cart_items.objects.create(
            cart = cart,
            product = item,
        )
    
    
    return redirect('product', product_uuid=product_uuid)

def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(is_paid = False, user = user)
        items = cart_items.objects.filter(cart = cart)
        if not items.exists():
            context = {"carts": cart, "message":"no items"}
        else:
            context = {"carts": cart}
    except Cart.DoesNotExist:
        context= {"message":"No items in cart"}
    return render(request, "cart.html", context)

def delete_cart_items(request, product_uuid):
    item = cart_items.objects.get(product_uuid = product_uuid)
    item.delete()
    return redirect('/cart/')

def checkout_page(request, id):
    user = request.user
    cart = Cart.objects.get(product_uuid=id,is_paid = False, user = user)
    amount = Cart.get_cart_total(cart)
    amount = amount['product__discounted_price__sum']

    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        Address = request.POST.get('Address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        phone_number = request.POST.get('phone_number')
        method = request.POST.get('method')
        pincode = request.POST.get('pincode')
        
        checkout.objects.get_or_create(
            name = name,
            email = email,
            phone_number = phone_number,
            Address = Address,
            state = state,
            city = city,
            amount = amount,
            user = user,
            method = method,
            pincode = pincode
        )

        items = cart_items.objects.filter(cart = cart)
        p_names = []
        sizes = []
        for item in items:
            p_names.append(item.product.product_name)
            sizes.append(item.size)

        subject = 'Order placed Succesfully'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['syb26633@gmail.com', ]
        message = f'{name}, Ordered \n{p_names}\nsize:{sizes} \ntotal-> ₹{amount}\nAddress: {Address}\nPhoneNumber:{phone_number}\nEmail:{email}\ncity:{city}\npincode:{pincode}\nstate:{state}'

        sub = 'Order placed Succesfully'
        msg = f'Hii {name} Your order have been succesfully placed\nThanks for ordering in EYN Store\nYou will recieve your product tracking link soon\nThankYou'
        rcp_list = [email]
        send_mail( sub, msg, email_from, rcp_list )

        mail = EmailMessage(subject= subject,body=message, from_email=email_from, to = recipient_list, )
        for item in items:
            image = item.product.product_image
            mail.attach_file(f"{settings.BASE_DIR}/{image}")
        mail.send()
        Cart.objects.filter(product_uuid=id,is_paid = False, user = user).update(is_paid=True)
        return redirect('/order-placed/')
    return render(request, "checkout.html")

def add_wishlist(request, product_uuid):
    user = request.user
    item = products.objects.get(product_uuid=product_uuid)
    wishlist.objects.get_or_create(
        user = user,
        product = item
    )
    return redirect('product', product_uuid=product_uuid)

def delete_wishlist(request, product_uuid):
    item = wishlist.objects.get(product__product_uuid=product_uuid)
    item.delete()
    return redirect('/wishlist/')

def wishlist_page(request):
    user = request.user
    items = wishlist.objects.filter(user=user)
    if not items.exists():
        context={"message":"Your wishlist is empty"}
    else:
        length = len(cart_items.objects.filter(cart__user = user, cart__is_paid = False))
        w_length = len(wishlist.objects.filter(user=user))
        context = {"items":items,"length":length,"w_length":w_length}
    return render(request,"wishlist.html",context)

def order_placed(request):

    return render(request, "order_placed.html")

def orders_page(request):
    user = request.user
    try:
        orders = Cart.objects.filter(is_paid=True, user=user)
        c_items = cart_items.objects.filter(cart__user=user, cart__is_paid=True)
        context = {"c_items": c_items}
        
        if not c_items.exists():
            context["message"] = "No items in the orders"
    except Cart.DoesNotExist:
        context = {"message": "No orders found"}

    return render(request, "orders.html", context)