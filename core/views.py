from django.shortcuts import render
from .models import ShipList
from .forms import SearchFrom


def ship_list(request):
    ships = ShipList.objects.get(id=6)
    return render(request,
                  'core/base.html',
                  {'ships': ships})


def ship_search(request):
    form = SearchFrom()
    if 'query' in request.GET:
        form = SearchFrom(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = ShipList.objects.filter(ship__icontains=cd)
    return render(request,
                  'core/base.html',
                  {'form': form,
                   'results': results})
