from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser, User

from utility.help_function import getrequest

class UserAuthentication(BaseAuthentication):

    def authenticate(self, request):
        data = getrequest(request)
        token = data['token']

        if not token:
            raise exceptions.AuthenticationFailed('Not a Valid User!')
        try:
            user = User.objects.get(id=pk)
            return user, True
        except User.DoesNotExist:
            return AnonymousUser(),None