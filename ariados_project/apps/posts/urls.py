from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/', views.get_post),
    url(r'^filter/', views.filter_posts),
    url(r'^my/', views.filter_my_posts),
    url(r'^save/', views.save_post),
]
