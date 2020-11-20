from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from urllib.parse import urlencode
from utility.decorators import login_required,logout_required
import requests
import json

from .models import *

LOCALHOST = 'http://127.0.0.1:8000/'

@logout_required
def login_view(request):
    if request.method == 'POST':
        data = request.POST
        URL = LOCALHOST + 'apis/login/'
        r = requests.post(url=URL,data=data)
        response = r.json()
        if response['res']:
            base_url = reverse('orders')
            res =  redirect(base_url)
            res.set_cookie('token',response['token'])
            return res
        base_url = '/'
        query_string = urlencode({'error': 'Invalid Credentials!!'})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    ctx = {'error':''}
    if 'error' in request.GET:
        ctx['error'] = request.GET['error']
    return render(request,'login_view.html',context=ctx)

@login_required
@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
@logout_required
def register_user(request):
    data = request.POST
    URL = LOCALHOST + 'apis/'
    r = requests.post(url=URL,data=data)
    return JsonResponse(json.loads(r.content))

@login_required
def orders(request):
    token = request.COOKIES['token']
    URL = LOCALHOST + 'apis/order_list/'
    r = requests.get(url=URL,headers={'Authorization':'Token '+token})
    response = r.json()
    if not response['res']:
        base_url = '/'
        query_string = urlencode({'error': response['error']})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    return render(request, 'order_list.html',context=response)

@login_required
def new_order(request):
    token = request.COOKIES['token']
    URL = LOCALHOST + 'apis/newOrder/'
    r = requests.get(url=URL, headers={'Authorization':'Token '+token})
    response = r.json()
    if not response['res']:
        base_url = '/'
        query_string = urlencode({'error': response['error']})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    return render(request,'new_order.html',context=response)

@login_required
@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        token = request.COOKIES['token']
        URL = LOCALHOST + 'apis/saveOrder/'
        r = requests.post(url=URL, data=request.POST,headers={'Authorization':'Token '+token})
        response = r.json()
        if not response['res']:
            base_url = '/'
            query_string = urlencode({'error': response['error']})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        return redirect('/orders/')
    return redirect('/')

@login_required
def order(request,id):
    token = request.COOKIES['token']
    URL = LOCALHOST + 'apis/viewOrder/'
    r = requests.get(url=URL, params={'id':id},headers={'Authorization':'Token '+token})
    response = r.json()
    if not response['res']:
        base_url = '/'
        query_string = urlencode({'error': response['error']})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    return render(request, 'view_order.html', context=response)


@login_required
def edit_order(request,id):
    if request.method == 'POST':
        return redirect('/')
    token = request.COOKIES['token']
    URL = LOCALHOST + 'apis/viewOrder/'
    r = requests.get(url=URL, params={'id': id},headers={'Authorization':'Token '+token})
    response = r.json()
    if not response['res']:
        base_url = '/'
        query_string = urlencode({'error': response['error']})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    ctx = response
    ctx.update({'id':id})
    return render(request, 'edit_order.html', context=ctx)

@login_required
@csrf_exempt
def update_order(request):
    data = request.POST
    status = data['status']
    remarks = data['remarks']
    id = data['id']

    Order.objects.filter(id=id).update(status=status,remarks=remarks)

    return redirect('/orders/')