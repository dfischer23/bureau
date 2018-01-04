from django.conf.urls import url, include

from . import views

from .models import Student

from rest_framework import routers, serializers, viewsets

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'short_name', 'name', 'first_name', 'dob')

class StudentViewSet(viewsets.ModelViewSet):
#    queryset = Student.objects.order_by('short_name')
    serializer_class = StudentSerializer
    def get_queryset(self):
    	queryset = Student.objects
    	status = self.request.query_params.get("status", "active")
    	queryset = queryset.filter(status=status)
    	return queryset.order_by('short_name')


router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, "students")

urlpatterns = [
#    url(r'^$', views.index, name='index'),
    url(r'^adressliste$', views.list_excel, name='adressliste'),
#    url(r'^students$', views.students_csv, name='students'),
	url(r'^students_csv/(?P<status>\w+)/$', views.students_csv),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
