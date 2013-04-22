from django.conf.urls.defaults import patterns, include, url
import app1.views

urlpatterns = patterns('app1',
    url(r'^$', 'views.main'),
    url(r'^get_details$', 'views.get_details'),
    url(r'^edit_row', 'views.edit_row'),
)
