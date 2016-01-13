from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^data/$', views.loadData, name='loadData'),
	url(r'^(?P<image_file>[-\w]+)/(?P<graph_num>[0-9]+)/(?P<graph_count>[0-9]+)/$', views.next, name='next'),
	url(r'^(?P<image_file>[-\w]+)/(?P<graph_num>[0-9]+)/(?P<graph_count>[0-9]+)/(?P<point_1_x>\d+\.\d{2})/(?P<point_1_y>\d+\.\d{2})/(?P<point_2_x>\d+\.\d{2})/(?P<point_2_y>\d+\.\d{2})/$', views.actionData, name='actionData'),
]