from django.shortcuts import render
from django.http import HttpResponse
from .models import ShipList
from .forms import SearchFrom


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

