from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [

    path('',views.home, name='home'),

    path('store/<int:pk>/',views.store, name='store'),
    path('store/<int:pk>/<int:pk2>',views.store, name='store'),
    path('store/<int:pk>/<int:pk2>/<int:pk3>',views.store, name='store'),
    path('product_details/<int:pk>',views.product_details, name='product_details'),
    path('checkout/',views.checkout, name='checkout'),
    path('payment/<int:pk>', views.payment, name='payment'),
    
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:pk>', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
