from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/mark_as_complete$', views.mark_complete, name='mark_as_complete'),
    url(r'^dashboard/mark_as_uncomplete$', views.mark_incomplete, name='mark_as_uncomplete'),
    url(r'^classes$', views.class_view, name='classes'),
    url(r'^classes/(\d+)$', views.single_class_view, name='single class'),
    url(r'^classes/updateStudent$', views.update_student, name='update student'),
    url(r'^settings$', views.settings_view, name='settings'),
    url(r'^settings/([a-zA-Z]+)$', views.settings_adjust, name='manage settings'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^attachment/([a-zA-Z\d]+)$', views.attachment_get, name='attachment'),
    url(r'^updateSQL', views.update_sql, name='updateSQL')
]
