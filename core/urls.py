from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.ship_search,
        name='ship_search'),

    url(r'^get_ship',
        views.get_ship,
        name='get_ship'),

    url(r'^(?P<ship>[-\w]+)/$',
        views.ship_detail,
        name='ship_detail'),

    # find_me
    url(r'^find_me',
        views.find_me,
        name='find_me'),

    # contact_me
    url(r'^contact',
        views.contact,
        name='contact'),
]
