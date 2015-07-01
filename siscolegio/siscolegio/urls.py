from django.conf.urls import patterns, include, url

from django.contrib import admin

from inicio import views

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'siscolegio.views.home', name='home'),
    url(r'^$', views.inicio, name="inicio_redirect"),
    url(r'^ameliagallegos/', include('inicio.urls', namespace='inicio')),
    url(r'^sisacademico/', include('sisacademico.urls', namespace='sisacademico')),
    url(r'^admin/', include(admin.site.urls)),
)
