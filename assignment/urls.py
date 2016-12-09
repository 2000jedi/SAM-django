from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/mark_as_complete$', views.markComplete, name='mark_as_complete'),
    url(r'^dashboard/mark_as_uncomplete$', views.markUnComplete, name='mark_as_uncomplete'),
    url(r'^classes$', views.class_view, name='classes'),
    url(r'^classes/(\d+)$', views.single_class_view, name='single_class'),
    url(r'^settings$', views.settings_view, name='settings'),
    url(r'^settings/([a-z,A-Z]+)$', views.settings_adjust, name='manage_settings'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^attachment/([a-z,A-Z,0-9]+)$', views.attachment_get, name='attachment'),
]
