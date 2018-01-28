from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/(?P<id>[0-9]+)$', views.get_trainer),
    url(r'^filter/', views.filter_trainers),
]
