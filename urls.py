from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^-----/', include(admin.site.urls)),
    url(r'', include('main.urls')),

)
