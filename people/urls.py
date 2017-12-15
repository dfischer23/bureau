from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^adressliste$', views.list_excel, name='adressliste'),
#    url(r'^students$', views.students_csv, name='students'),
	url(r'^students_csv/(?P<status>\w+)/$', views.students_csv),
]
