from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register, name="register"),
    path('login_page/',views.login_page, name="login"),
    path('seller_register/',views.seller_register, name="seller_register"),
    path('seller_login/',views.seller_login, name="seller_login"),
    path('logout_page/',views.logout_page, name="logout"),
    path('seller_dashboard/',views.seller_dashboard, name="seller_dashboard"),
    path('add_product/',views.add_product, name="add_product"),
    path('add_seller_product/',views. add_seller_product, name="add_seller_product"),
    path('product_detail/<int:id>',views.product_detail, name="product_detail"),
    path('approve_product/<int:id>',views.approve_product, name="approve_product"),
    path('delete_product/<int:id>',views.delete_product, name="delete_product"),
    path('delete_seller_product/<int:id>',views.delete_seller_product, name="delete_seller_product"),
    path('product_list',views.product_list, name="product_list"),
    path('admin_request',views.admin_request, name="admin_request"),
    path('error_page',views.error_page, name="error_page"),
    path('shop_page/',views.shop_page, name="shop_page"),
    path('search/',views.search, name="search"),
    path('cart_view/',views.cart_view, name="cart_view"),
    path('add_to_cart/<int:id>',views.add_to_cart, name="add_to_cart"),
    path('delete/<int:id>',views.delete, name="delete"),
    path('payment/',views.payment, name="payment"),
    path('tracking/<int:id>',views.tracking_view, name="tracking"),
    path('profileset/',views.profileset, name="profileset"),
    path('base_view/',views.base_view, name="base_view"),
    path('category/',views.category, name="category"),

    path('pending_seller_products/', views.pending_seller_products, name='pending_seller_products'),
    path('approve_seller_product/<int:product_id>/', views.approve_seller_product, name='approve_seller_product'),
    path('reject_seller_product/<int:product_id>/', views.reject_seller_product, name='reject_seller_product'),

]