from django.shortcuts import render
from django.http import HttpResponse

from .models import ShipList
from .forms import SearchFrom

import json


def ship_search(request):
    """Returns query with ship object."""
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


def get_ship(request):
    """jQuery Autocomplete function makes ajax call by itself.
    When user types a string in autocomplete input field, an AJAX
    call is made with the ID of the input field to autocomplete
    function of Jquery-ui. In the source property, a url is supplied
    which maps to a django view. Then in view we query the model
    we want to with the parameter named 'term', eg. the term contains
    “HMS”, a list is generated containing the 'term'."""
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
