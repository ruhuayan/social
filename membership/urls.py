from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile', views.profile),
    url(r'^add/group', views.add_group),
    url(r'^add/users/(?P<groupName>[\w\s]+)$', views.add_group_user),
    url(r'^confirm/(?P<invite_id>\d+)/(?P<accept>\d)$', views.confirm_invite),
    url(r'^group$', views.group),
    url(r'^edit/(?P<groupName>\w+)$', views.edit_group),
    url(r'^delete/(?P<groupName>\w+)$', views.delete_group),
    url(r'^membership/(?P<groupName>\w+)$', views.member_group),
    url(r'^message/$', views.message),
    url(r'^message/(?P<mid>\d+)$', views.message),
    url(r'^$', views.profile),
]