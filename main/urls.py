from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^(.+)/$', 'main.views.user_link', name='home')
)
