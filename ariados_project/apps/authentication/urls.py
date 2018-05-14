from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', include('rest_auth.urls')),
    url(r'^login/', views.handle_login),
    url(r'^logout/', views.handle_logout),
    url(r'^users/', views.show_users),
    # url(r'^restringido/', views.show_forbidden),
]