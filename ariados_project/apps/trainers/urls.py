from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/(?P<id>[0-9]+)$', views.get_trainer),
    url(r'^filter/', views.filter_trainers),
    url(r'^test/', views.show_test),
    url(r'^save/', views.save_trainer),
    url(r'^send_friend_request/', views.send_friend_request),
]
