from django.shortcuts import render
from .models import ShipList


def ship_list(request):
    ships = ShipList.objects.get(id=6)
    return render(request,
                  'core/base.html',
                  {'ships': ships})
