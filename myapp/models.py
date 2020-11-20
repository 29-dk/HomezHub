from django.db import models
from django.contrib.auth.models import User

from utility.choices import *

class UserDetails(models.Model):
    user = models.OneToOneField(User,related_name='user_detail',db_index=True,on_delete=models.CASCADE,primary_key=True)
    primarynumber = models.IntegerField()
    primarycode = models.CharField(max_length=10)
    alt_number = models.IntegerField(blank=True,null=True)
    alt_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name

    class Meta:
        db_table = 'user_details'


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'state'


class Order(models.Model):
    user = models.ForeignKey(User,related_name='user_order',db_index=True,on_delete=models.CASCADE)
    order_type = models.CharField(max_length=100,choices=ORDER_TYPE)
    description = models.TextField()
    status = models.CharField(max_length=100,choices=ORDER_STATUS,blank=True,null=True)
    remarks = models.TextField(blank=True,null=True)
    pincode = models.IntegerField()
    city = models.CharField(max_length=200,blank=True,null=True)
    state = models.ForeignKey(State,related_name="state_order",on_delete=models.CASCADE,db_index=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        db_table = 'order'
