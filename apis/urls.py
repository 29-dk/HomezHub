from django.urls import path
from .views import *

urlpatterns = [
    path('',SignupApi.as_view()),
    path('login/',LoginApi.as_view()),
    path('order_list/',OrderList.as_view()),
    path('newOrder/',NewOrder.as_view()),
    path('saveOrder/',SaveOrder.as_view()),
    path('viewOrder/',ViewOrder.as_view()),
]