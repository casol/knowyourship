from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse

from .models import ShipList
from .forms import SearchForm

import itertools
from haystack.query import SearchQuerySet

import requests


def ship_detail(request, ship):
    ship = get_object_or_404(ShipList, slug=ship)
    return render(request,
                  'core/draft/details.html',
                  {'ship': ship})


def find_me(request):
    query = request.GET.get('query', '')
    if query:
        results = SearchQuerySet().models(ShipList).filter(content=query).load_all()
    else:
        results = None
    return render(request,
                  'core/draft/find_me.html',
                  {'results': results,
                   'query': query})
"""
def find_me_by_ip(request):
    geolocation = requests.get('http://ip-api.io/api/json')
    geolocation_json = geolocation.json()
    country = geolocation_json['country_name']
    results = SearchQuerySet().models(ShipList).filter(content=country).load_all()
    return render(request,
                  'core/draft/find_me.html',
                  {'results': results,
                   'country': country})
"""


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
                   'results': results})


def get_ship(request):
    """jQuery Autocomplete function makes ajax call by itself.
    When user types a string in autocomplete input field, an AJAX
    call is made with the ID of the input field to autocomplete
    function of Jquery-ui. In the source property, a url is supplied
    which maps to a django view. Then in view we query the model
    with the parameter named 'term'.
    """
    # haystack autocomplete in progress
    query = request.GET.get('term', '')
    sqs = SearchQuerySet().autocomplete(text=query)[:5]
    suggestions = [result.text for result in sqs]  # <---- RESULT.OBJECT.SHIP RESULT.OBJECT.country !!
    # list of all country from ShipList model      # omg... just need to be sugg_ship and sugg_contry
    country_list = ShipList.objects.all().values_list('country', flat=True)
    country_list = list(set(country_list))
    # split string into a list e.g. "USS Becun\nUnited States\n" -> ["USS Becun, "United", ""]
    results = [ship.split('\n') for ship in suggestions]
    # make list out of list of lists e.g. [[1, 2],[4, 5]] -> [1, 2, 4, 5]
    results = list(itertools.chain.from_iterable(results))
    # remove empty strings from a list
    results = list(set(filter(None, results)))
    # check if query contains country name
    if any(query.title() in s for s in country_list):
        # compere two lists and return matches
        compere = list(set(results) & set(country_list))
        results = []
        # return country
        results = compere
    else:
        # if query contains ship name remove country from results
        results = list(set(results) - set(country_list))
    # Make sure you return a JSON object, not a bare list.
    # if other than dict you must set the safe parameter to False
    return JsonResponse(results, safe=False)
