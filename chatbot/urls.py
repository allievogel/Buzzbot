from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^chat$', views.chat, name='chat'),
    # url(r'^brief$', views.brief, name='brief')

]
