from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.show_login),
    url(r'^login/', views.handle_login),
    url(r'^logout/', views.handle_logout),
    # url(r'^restringido/', views.show_forbidden),
]