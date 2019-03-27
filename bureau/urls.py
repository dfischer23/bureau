
from django.conf.urls import include,url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^people/', include('people.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/admin'))
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

admin.site.site_header = "Infinita Bureau"
