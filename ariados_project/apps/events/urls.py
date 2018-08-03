from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update/$', views.get_pgo_events),
    url(r'^$', views.get_last_events),
]
