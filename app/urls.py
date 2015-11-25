# app/urls.py

from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^profile/$', views.profile, name='profile'),
    url('^profile/repo/$',views.get_token, name='repo'),
    url(r'^github-callback/$', views.github_callback, name='github-callback'),
   	url(r'^get-repo/$', views.show_repository, name='get-repo'),
   	url(r'^create-repo/$', views.create_repo,  name='create-repo'),
]
