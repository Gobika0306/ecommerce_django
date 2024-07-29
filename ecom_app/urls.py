from django.urls import path
from . import views
from .views import *
from .views import register, login_view
from .views import admin_only_view, unauthorized_view



urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/',views.home,name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),

    # CRUD URLs
    path('users/', views.list_users, name='list_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-page/', admin_only_view, name='admin_page'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
    path('manager/', manager_only_view, name='manager_page'),
    path('shop/order/<int:product_id>/', order_product, name='order_product'),
    path('shop/order/success/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),

]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)