from django.contrib import admin
from django.urls import path
from . import views 
from .views import CreateStripeCheckoutSessionView

urlpatterns = [
    path('',views.index,name='index'),
    path('shop',views.shop,name='shop'),
    path('account/login',views.login1,name='login'),
    path('logout',views.logout_view,name='log'),
    path('account/register',views.register,name='register'),
    path('accounts',views.accounts,name='accounts'),
    path('compare',views.compare,name='compare'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('details',views.details,name='details'),
    path('checkout',views.checkout,name='checkout'),
    path('placeOrder',views.placeOrder,name='placeOrder'),
    path('thankyou',views.thankyou,name='thankyou'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart_detail',views.cart_detail,name='cart_detail'),

     path(
        "create-checkout-session/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
     ),
]