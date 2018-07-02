from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/', views.get_trainer),
    url(r'^filter/', views.filter_trainers),
    url(r'^test/', views.show_test),
    url(r'^save/', views.save_trainer),
    url(r'^send_friend_request/', views.send_friend_request),
    url(r'^get_friend_requests/', views.get_friend_requests),
    url(r'^accept_friend_request_from/', views.accept_friend_request_from),
    url(r'^reject_friend_request_from/', views.reject_friend_request_from),
    url(r'^get_friends/', views.get_friends),
    url(r'^update_location/', views.update_location),
]
