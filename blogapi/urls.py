from blogapi import views
from django.conf.urls import url

urlpatterns = [
    url(r'^create/user/$', views.create_user),
    url(r'^create/article/$', views.create_blog),
    url(r'^create/comment/$', views.create_comment),

    url(r'^login/$', views.login_user),

    url(r'^update/article/$', views.update_blog),
    url(r'^delete/article/$', views.delete_blog),
]
