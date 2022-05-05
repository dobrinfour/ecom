from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

app_name = 'showroom_admin'

urlpatterns = [

    path('',views.dashboard, name='dashboard'),
    
    path('order_detail/<int:pk>',views.orderdetail, name='orderdetail'),
    path('send/<int:pk>',views.send, name='send_order'),
    path('product_list/',views.productList, name='productlist'),
    path('product_item/<int:pk>',views.productItem, name='product_item'),
    path('add_product/',views.add_product, name='add_product'),
    path('edith_product/<int:pk>',views.edith_product, name='edith_product'),
    path('delete_product/<int:pk>',views.delete_product, name='delete_product'),

    path('category_list/',views.category_list, name='category_list'),
    path('add_category/',views.add_category, name='add_category'),

    path('delete_category/<int:pk>',views.delete_category, name='delete_category'),

    path('pending_list/',views.pending_list, name='pending_list'),
    path('delivered_list/',views.delivered_list, name='delivered_list'),
    path('login/',views.my_login, name='login'),
    path('delete_category/<int:pk>',views.delete_category, name='delete_category'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
