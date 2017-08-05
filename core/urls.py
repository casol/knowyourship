from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^search/', views.ship_search, name='ship_search'),
    url(r'^$', views.ship, name='ship'),
    url(r'^get_ship', views.get_ship, name='get_ship'),

]
