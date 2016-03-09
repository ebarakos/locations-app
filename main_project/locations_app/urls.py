from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^saveLocation$', views.saveLocation, name='saveLocation'),
    url(r'^delete$', views.delete, name='delete'),
]
