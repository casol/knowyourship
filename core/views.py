from django.shortcuts import render
from django.http import HttpResponse
from .models import ShipList
from .forms import SearchFrom
import json


def ship_list(request):
    ships = ShipList.objects.get(id=6)
    return render(request,
                  'core/index.html',
                  {'ships': ships})


def ship_search(request):
    form = SearchFrom()
    results = None
    cd = None
    if 'query' in request.GET:
        form = SearchFrom(request.GET)
        if form.is_valid():
            cd = form.cleaned_data['query']
            # get attribute 'ship' and return list of values
            #results = ShipList.objects.filter(ship__icontains=cd).values_list('ship', flat=True)
            results = ShipList.objects.filter(ship__icontains=cd)
    return render(request,
                  'core/draft/search.html',
                  {'form': form,
                   'results': results,
                   'cd': cd})


def auto_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        ships = ShipList.objects.filter(ship__icontains=q)
        results = []
        for ship in ships:
            ship_json = {}
            ship_json = ship.ship
            results.append(ship_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

