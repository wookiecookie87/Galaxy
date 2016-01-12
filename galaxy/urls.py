from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<image_file>[-\w]+)/(?P<graph_num>[0-9]+)/(?P<graph_count>[0-9]+)/$', views.next, name='next'),
	url(r'^(?P<image_file>[-\w]+)/(?P<graph_num>[0-9]+)/(?P<graph_count>[0-9]+)/(?P<point_1_x>[0-9]+)/(?P<point_1_y>[0-9]+)/(?P<point_2_x>[0-9]+)/(?P<point_2_y>[0-9]+)/$', views.actionData, name='actionData'),
]