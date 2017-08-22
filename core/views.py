from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import ShipList
from .forms import SearchFrom

import json


def ship_detail(request, ship):
    ship = get_object_or_404(ShipList, slug=ship)
    return render(request,
                  'core/draft/details.html',
                  {'ship': ship})


def ship_list_by_country(request):
    pass


def ship_search(request):
    """Returns query with ship object or queryset with list
    of ships from requested country.
    """
    form = SearchFrom()
    results = None
    cd = None
    if 'query' in request.GET:
        form = SearchFrom(request.GET)
        if form.is_valid():
            cd = form.cleaned_data['query']
            # get attribute 'ship' and return list of values
            # results = ShipList.objects.filter(ship__icontains=cd).values_list('ship', flat=True)
            try:
                result = ShipList.objects.get(ship__icontains=cd)
                if result:
                    return redirect(result)
            except ShipList.DoesNotExist:
                results = ShipList.objects.filter(country__icontains=cd)

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
    with the parameter named 'term', eg. the term contains
    “HMS”, a list is generated containing the 'term'.
    """
    if request.is_ajax():
        q = request.GET.get('term', '')
        ships = ShipList.objects.filter(
            Q(ship__icontains=q) | Q(country__icontains=q)).distinct()
        results = []
        for ship in ships:
            ship_json = {}
            ship_json = ship.ship
            country_json = ship.country
            if country_json not in results:
                results.append(country_json)
            results.append(ship_json)
            # results = list(set(results))
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
