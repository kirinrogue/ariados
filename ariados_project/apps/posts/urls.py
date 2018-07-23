from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/', views.get_post),
    url(r'^filter/', views.filter_trainers),
    url(r'^save/', views.save_trainer),
]
