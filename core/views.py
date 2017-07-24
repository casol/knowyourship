from django.shortcuts import render
from .models import ShipList


def ship_list(request):
    ships = ShipList.objects.all()
    return render(request,
                  'core/index.html',
                  {'ships': ships})
