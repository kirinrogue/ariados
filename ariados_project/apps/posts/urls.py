from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/', views.get_post),
    url(r'^filter/', views.filter_posts),
    url(r'^my/', views.filter_my_posts),
    url(r'^answers/', views.get_answers),
    url(r'^save/', views.save_post),
    url(r'^events/', views.get_pgo_events),
]
