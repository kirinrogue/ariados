from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/', views.get_post),
    url(r'^filter/', views.filter_posts),
    url(r'^my/', views.filter_my_posts),
    url(r'^answers/', views.get_answers),
    url(r'^delete/', views.delete_post),
    url(r'^create/', views.create_post),
    url(r'^update/', views.update_post),
    url(r'^answer/', views.answer_post),
    url(r'^votes/', views.get_votes),
    url(r'^vote/', views.vote_post),
    url(r'^is_author/', views.is_author),
]
