from django.urls import path
from .views import *

urlpatterns = [
    path('',login_view,name='login_view'),
    path('logout/',logout_view,name='logout_view'),
    path('register/',register_user,name='register'),
    path('orders/',orders,name='orders'),
    path('order/<id>/',order,name='order'),
    path('new_order/',new_order,name='new_order'),
    path('save_order/',save_order,name='save_order'),
    path('edit_order/<id>/',edit_order,name='edit_order'),
    path('update_order/',update_order,name='update_order'),
]