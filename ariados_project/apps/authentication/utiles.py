from django.contrib.auth import authenticate, login


# Function to handle authentication, we first authenticate by default in Django (user,pass),
#   and if we were successful (user really exists in database), we login through Django's default login functionality
def handle_auth(request, name, password):
    assert isinstance(name, str)
    assert isinstance(password, str)
    user = authenticate(username=name, password=password)
    if user is None:
        raise Exception('Email o contraseña incorrectos.')
    else:
        login(request, user)
    return user
