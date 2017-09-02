from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import ShipList
from .forms import SearchForm

import json
import itertools
from haystack.query import SearchQuerySet


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
    results = None
    cd = None
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(ShipList).filter(content=cd['query']).load_all()

    return render(request,
                  'core/draft/search.html',
                  {'form': form,
                   'results': results,
                   'cd': cd})


def get_ship(request):
    # haystack autocomplete in progress

    sqs = SearchQuerySet().autocomplete(text=request.GET.get('term', ''))[:5]
    suggestions = [result.text for result in sqs]
    clean_sug = []
    for ship in suggestions:
        clean_sug.append(ship.split('\n'))
    clean_sug = list(itertools.chain.from_iterable(clean_sug))
    clean_sug = list(filter(None, clean_sug))

    """
    q = request.GET.get('term', '')
    sqs = SearchQuerySet().models(ShipList)
    sqs1 = sqs.filter(ship_auto=q)
    sqs2 = sqs.filter(country_auto=q)
    sqs = sqs1 | sqs2
    suggestions = []
    # list of country
    # list(set(source))
    country_list = ShipList.objects.all().values_list('country', flat=True)
    country_list = list(set(country_list))
    #suggestions = [result.ship_auto for result in sqs]
    for result in sqs:
        suggestions.append(result.ship_auto)
        if result.country_auto not in suggestions:
            suggestions.append(result.country_auto)
            if result.country_auto in country_list:
                suggestions.insert(0, result.country_auto)
    """
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps(
        clean_sug
    )
    return HttpResponse(the_data, content_type='application/json')

'''
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
'''