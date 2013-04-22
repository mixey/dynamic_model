from django.conf.urls.defaults import patterns, include, url
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^app1/', include('app1.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        (r'^media/(.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
