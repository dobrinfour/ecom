from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [

    path('',views.home, name='home'),
    path('product_details/<int:pk>',views.product_details, name='product_details'),
    path('checkout/',views.checkout, name='checkout'),
    path('payment/<int:pk>', views.payment, name='payment'),
    path('faker_data/',views.faker_data, name='faker_data'),
    
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:pk>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),

]
