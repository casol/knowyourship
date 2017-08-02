from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ship_search, name='ship_search'),
    url(r'^search/$', views.auto_search, name='auto_search'),

]
