from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<target_id>[0-9]+)/$', views.target, name='target'),
    url(r'(?P<target_id>[0-9]+)/(?P<attribute>[a-zA-Z\-]+)/', views.dynamic_raster, name='dynamic_raster')
]