from django.shortcuts import render
from .models import ShipList
from .forms import SearchFrom


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
            results = ShipList.objects.filter(ship__icontains=cd)
            results = list(results)
    return render(request,
                  'core/search.html',
                  {'form': form,
                   'results': results,
                   'cd': cd})
