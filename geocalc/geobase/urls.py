from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^edit_project/(?P<project_id>[0-9]+)/$', views.edit_project, name='edit_project'),
    url(r'^delete_project/(?P<project_id>[0-9]+)/$', views.delete_project, name='delete_project'),
    url(r'^new_project/', views.new_project, name='new_project'),
]