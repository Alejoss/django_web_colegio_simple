from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'siscolegio.views.home', name='home'),
    url(r'^ameliagallegos/', include('inicio.urls', namespace='inicio')),
    url(r'^admin/', include(admin.site.urls)),
)
