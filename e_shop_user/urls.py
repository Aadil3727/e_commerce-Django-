from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.reg, name='signup'),
        path('', views.home, name='home-page'),
        path('login-user/', views.user_login, name='login-user'),
        path('logout-user/', views.user_logout, name='logout-user'),
        path('product-details/<str:slug>', views.product_details, name='pro-det'),
        path('cart-view/', views.cart_view, name='cart-view'),
        path('add-cart/<str:slug>', views.add_to_cart, name='add-to-cart'),
        path('del-cart-item/<str:slug>', views.del_cart_item, name='del-cart-item'),
        path('add-cart-item/<str:slug>', views.add_cart_item, name='add-cart-item'),
        path('del-all-cart/<str:slug>', views.del_all_cart, name='del-all-cart'),
        path('shop-products/', views.PostsView.as_view(), name='allproducts'),
        path('reset-password/', views.forget_password, name="reset-pass"),
        path('change-password/<token>/', views.change_password, name="change-password"),
        path('wish-list/', views.wish_list, name="wish-lists"),
        path('add-to-wishlist/<int:pk>', views.add_to_wishlist, name="add-to-wishlist"),
        path('del-wishlist/<int:pk>', views.del_wishlist, name="del-wishlist"),
        path('user-profile/<str:slug>', views.user_profile, name="user-profile"),
        path('all-cate/', views.all_cate, name="all-cate"),
        path('pro-by-cate/<str:slug>', views.cate_pro, name="cate-pro"),
        path('page-not-found/', views.page_not_found, name="page-not-found"),
        path('contact-us/', views.contact_us, name="contact-us"),
]