from django.urls import path
from . import views
from .views.signup import Signup
from .views.login import Login, logout
from .views.home import Detail, Index
from .views.post import post_detail, post_list, video, aboutus, cart
from .views.store import store, search, product_list, cart_view, add_to_cart, remove_from_cart,update_cart_quantity,create_order,order_success
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),
    path('logout', logout , name='logout'),
    path('detail/', Detail.as_view(), name='product-detail'),
    path('post', post_list, name='post'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('video', video, name='video'),
    path('aboutus', aboutus, name='aboutus'),
    path('signup', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('cart', cart, name='cart'),
    path('search/', search, name='search'),
    path('', product_list, name='product_list'),
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
     path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
     path('update-cart-quantity/<int:product_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('create-order/', create_order, name='create_order'),
     path('order-success/<int:order_id>/', order_success, name='order_success'),
    
]