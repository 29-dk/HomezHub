from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from urllib.parse import urlencode

def login_required(function):
    def wrapper(request, *args, **kw):
        if 'token' in request.COOKIES:
            token = request.COOKIES['token']
            try:
                Token.objects.get(key=token)
            except Token.DoesNotExist:
                base_url = '/'
                query_string = urlencode({'error': 'Please Login to Proceed!!'})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            return function(request, *args, **kw)
        else:
            base_url = '/'
            query_string = urlencode({'error': 'Please Login to Proceed!!'})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    return wrapper

def logout_required(function):
    def wrapper(request, *args, **kw):
        if 'token' in request.COOKIES:
            token = request.COOKIES['token']
            try:
                Token.objects.get(key=token)
                base_url = '/'
                query_string = urlencode({'error': 'You are Logged Out!!'})
                url = '{}?{}'.format(base_url, query_string)
                res =  redirect(url)
                res.delete_cookie('token')
                return res
            except Token.DoesNotExist:
                pass
        return function(request, *args, **kw)
    return wrapper
