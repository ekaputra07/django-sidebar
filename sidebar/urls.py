from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sidebar.views',
    url(r'^sidebar/$', 'ajax_load_widgets', name='load_sidebar'),
    url(r'^sidebar/add/$', 'ajax_add_to_sidebar', name='sidebar_add'),
    url(r'^sidebar/update/$', 'ajax_update_widget', name='update_widget'),
    url(r'^sidebar/reorder/$', 'ajax_reorder_widget', name='reorder_widget'),
    url(r'^sidebar/delete/$', 'ajax_delete_widget', name='delete_widget'),
)

