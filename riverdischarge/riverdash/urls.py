from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from riverdash import views

urlpatterns = [
	url(r'^devices/$',views.device_list),
	url(r'^devices/(?P<pk>[0-9]+)$', views.device_detail),
	url(r'^readings/$',views.reading_list),
	url(r'^readings/charting/$',views.get_reading_for_chart),
	url(r'^readings/reports/$',views.html_to_pdf),
	url(r'^readings/listing/$',views.readings_wpagination),
	url(r'^readings/reports/daily/$',views.daily_report),
	url(r'^machine/run/$', views.machine_learning),
	url(r'^index/$',views.index),
	url(r'^login/$',views.login_user),
	url(r'^login/now/$',views.login_now),
	url(r'^regression/calculate/$',views.get_regression_working),
	url(r'^$',views.index),
]

urlpatterns = format_suffix_patterns(urlpatterns)