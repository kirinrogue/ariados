# coding: utf-8
import json

from django.contrib.auth import logout

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
