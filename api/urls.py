from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', "api.views.index"),
    url(r'^calculate/$', "api.views.calculate"),
    url(r'^update/$', "api.views.update"),
    url(r'^geochat/$', "api.views.geochat"),
    url(r'^geochat_post/$', "api.views.geochat_post"),
)

