from django.shortcuts import render
from .models import Product, Compare, Wishlist, Order, OrderItem
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
# Create your views here.
def index(request):
         return render(request, 'web/index.html')
def shop(request):
    context = {
            'product': Product.objects.all()
         }  
    return render(request, 'web/shop.html',context)

def login1(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Invalid details')
                return redirect('register')
        return render(request, 'web/account/login.html')
def register(request):
        if request.method == "POST":
            username = request.POST.get("Username")
            firstname = request.POST.get("First_name")
            lastname = request.POST.get("Last_name")
            email = request.POST.get("Email")
            password = request.POST.get("Password")
            confirm_password = request.POST.get("Confirm_password")

            if password != confirm_password:
                messages.warning(request, 'Passwords do not match')
            else:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, 'User already exists')
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, 'Email already in use')
                else:

                    user = User.objects.create_user(username, email, password)
                    # -django inbuilt
                    user.first_name = firstname 
                    user.last_name = lastname

                    user.save()
                    return redirect('login')
        return render(request, 'web/account/register.html')
def logout_view(request):
    logout(request)
    return redirect('index')
    # Redirect to a success page.

# def cart_details(request):
#      return render(request, 'web/cart/cart_details.html')

@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("shop")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'web/cart/cart_detail.html')

def accounts(request):
     return render(request, 'web/accounts.html')

def compare(request):
     context = {
          "compare": Compare.objects.all()
     }
     return render(request, 'web/compare.html', context)

def wishlist(request):
     context = {
          'wishlist' : Wishlist.objects.all()
     }
     return render(request, 'web/wishlist.html', context)
def details(request):
     return render(request, 'web/details.html')

def checkout(request):
     return render(request, 'web/checkout.html')

def placeOrder(request):
    # Check if the request is POST
    if request.method == 'POST':
        # Get user ID from session
        uid = request.session.get('_auth_user_id')
        # Get user object
        user = User.objects.get(id=uid)

        # Get cart data from session
        cart = request.session.get('cart')

        # Get order details from request
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        country = request.POST.get('country')

        # Create Order instance
        order1 = Order(
            user = user,
            name = name,
            email = email,
            address = address,
            city = city,
            zipcode = zipcode,
            phone = phone,
            country = country,
        )
        # Save order to database
        order1.save()
        # Iterate through each item in cart and create an OrderItem instance for it
        for i in cart:
            a = float(cart[i]['price'])
            b = int(cart[i]['quantity'])
            total = a * b

            order3 = OrderItem(
                order = order1,
                image = cart[i]['image'],
                product = cart[i]['name'],
                quantity = cart[i]['quantity'],
                price =cart[i]['price'],
                total = total
            )
            order3.save()
    return render(request, 'web/placeOrder.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """
    def post(self, request, *args, **kwargs):
        # Get the total price of all items in the cart

        price_id = Product.objects.all()
        totalPrice=0
        for p in price_id:
            totalPrice += (p.price)
            name = p.name
            stripe.api_key = settings.STRIPE_SECRET_KEY
                

        # subtotal = 0
        # for item in price_id:
        #     subtotal += int(item.price)
        #     name = item.name
        #     # Calculate taxes based on your business needs (5% here)
        #     tax = round((subtotal + 12) / 100, 2)
        #     # Total amount is the sum of original price plus tax
        #     total = subtotal + tax
           

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": int(p.price) * 100,
                        "product_data": {
                            "name": name,
                            # "description": price.product.desc,
                            # "images": [
                            #     f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                            # ],
                        },
                    },
                    "quantity": 1,
                }
            ],
            # metadata={"product_id": price.product.id},
            mode="payment",
            success_url="http://localhost:8000/thankyou",
            cancel_url="http://localhost:8000/cancel",
        )
        return redirect(checkout_session.url)

def thankyou(request):
    return render(request, 'web/thankyou.html')


    