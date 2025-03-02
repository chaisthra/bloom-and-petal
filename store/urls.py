from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    # User account URLs
    path('account/', views.my_account, name='my_account'),
    path('account/orders/', views.my_orders, name='my_orders'),
    path('account/orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Product management URLs
    path('products/manage/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/import/', views.import_products, name='import_products'),
    
    # Category management URLs
    path('categories/manage/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
] 