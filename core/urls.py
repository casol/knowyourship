from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ship_list, name='ship_list'),
    url(r'^search/$', views.ship_search, name='ship_search'),

]
