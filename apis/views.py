from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate,login,logout

from myapp.models import *
from .authentication import UserAuthentication
from utility.help_function import getrequest
from utility.choices import ORDER_STATUS,ORDER_TYPE

class SignupApi(APIView):

    def post(self,request):
        data = getrequest(request)

        name = data['name']
        email = data['email']
        mobile = data['mobile']
        code = data['code']
        password = data['password']

        if ' ' in name:
            name = name.split(' ')
        else:
            name = [name, '']

        if User.objects.filter(email=email).exists():
            return Response({'res': 0, 'msg': 'Email Id Already Exists!'})
        try:
            with transaction.atomic():
                user = User.objects.create(email=email, first_name=name[0], last_name=name[1], username=email)
                user.set_password(password)
                user.save()
                UserDetails(user=user, primarynumber=mobile, primarycode=code).save()
            return Response({'res': 1, 'msg': 'Sign Up Completed!'})
        except Exception as e:
            print(e)
            return Response({'res': 0, 'msg': e.args})

class LoginApi(APIView):

    def post(self,request):
        data = getrequest(request)
        print(data)
        email = data['email']
        password = data['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'res':1,'msg':'Logged In Successfully!','token':token.key})
        else:
            return Response({'res':0,'msg':'Authentication Failed!','token':''})

class OrderList(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = request.user

        is_admin = False
        if user.groups.filter(name='Admin').exists():
            is_admin = True

        orders = Order.objects.filter(user=user) if not is_admin else Order.objects.all()
        arr = []
        for order in orders:
            if is_admin:
                href = "/edit_order/"+str(order.id)+"/"
                action = '<a target="_blank" href="'+href+'">Edit</a>'
            else:
                href = "/order/"+str(order.id)+"/"
                action = '<a target="_blank" href="'+href+'">View</a>'
            arr.append({
                'id' : 'Order-'+str(order.id),
                'type' : order.order_type,
                'desc' : order.description,
                'date' : order.timestamp.strftime("%d-%m-%Y"),
                'status' : order.status.title() if order.status else '-',
                'action': action
            })
        return Response({'data':arr,'res':1})

class NewOrder(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):

        order_type = []
        for tup in ORDER_TYPE:
            for val in tup:
                order_type.append(val)
                break

        states = State.objects.values_list('id','name')
        data = {
            'order_type':order_type,
            'states' : states
        }
        return Response({'res':1,'data':data})

class SaveOrder(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        data = getrequest(request)

        user = request.user

        Order.objects.create(user=user,order_type=data['order-type'],description=data['order-desc'],
                             pincode=data['pincode'],city=data['city'],state_id=data['state'])

        user_d = user.user_detail
        user_d.alt_number = data['mobile']
        user_d.alt_code = data['code']
        user_d.save()

        return Response({'res':1,'msg':'Done!'})

class ViewOrder(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        order_id = request.GET['id']

        user = request.user
        user_d = user.user_detail
        alt_no = user_d.alt_code+"-"+str(user_d.alt_number) if user_d.alt_code and user_d.alt_number else ''
        order = Order.objects.get(id=order_id)

        status_list = []
        for tup in ORDER_STATUS:
            for val in tup:
                status_list.append(val)
                break

        dictt = {
            'id':order.id,
            'type':order.order_type,
            'desc':order.description,
            'city':order.city,
            'state':order.state.name,
            'pin':order.pincode,
            'status':order.status,
            'status_list':status_list,
            'remark':order.remarks,
            'alt':alt_no
        }
        return Response({'res':1,'data':dictt})






