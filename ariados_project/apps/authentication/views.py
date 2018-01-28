# coding: utf-8
import json

from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import authentication

from .serializers import UserSerializer
from .utiles import *


# def show_login(request):
#     if request.user.is_authenticated():
#         return redirect('/')
#     else:
#         return render(request, 'autenticacion/login.html')


def handle_login(request):
    user_json = UserSerializer.create(request.POST)

    try:
        user = handle_auth(request, user_json.username, user_json.password)
        if user is not None:
            return json.dumps({'status': 'VALID', 'message': 'Successfully authenticated.'})
        else:
            return json.dumps(
                {'status': 'INVALID', 'message': 'Authentication error. Contact with the administrator.'})
    except:
        return json.dumps({'status': 'INVALID', 'message': 'Authentication error. Did you forget your password?'})


def handle_logout(request):
    logout(request)
    return json.dumps({'status': 'VALID', 'message': 'Successfully logged out.'})


@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def show_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def example_view(request, format=None):
#     content = {
#         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#         'auth': unicode(request.auth),  # None
#     }
#     return Response(content)