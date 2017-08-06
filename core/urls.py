from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ship_search, name='ship_search'),
    url(r'^get_ship', views.get_ship, name='get_ship'),

]
