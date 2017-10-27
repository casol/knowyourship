from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from .models import ShipList, Comment
from .forms import SearchForm, ContactForm, CommentForm

import itertools
from haystack.query import SearchQuerySet
import redis
from django.conf import settings

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

import requests


def ship_detail(request, ship):
    ship = get_object_or_404(ShipList, slug=ship)
    # increment total ship views by 1
    total_views = r.incr('ship:{}:views'.format(ship.id))
    # ship ranking increment by 1
    r.zincrby('ship_ranking', ship.id, 1)

    # list of active comments
    comments = ship.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.get(id=parent_id)
                if parent_qs:
                    parent_obj = parent_qs
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.ship = ship
            # save
            new_comment.save()
            # clear form field after a submit
            # comment_form = CommentForm()
            return HttpResponseRedirect(ship.get_absolute_url())
    else:
        comment_form = CommentForm()

    return render(request,
                  'core/portfolio.html',
                  {'ship': ship,
                   'total_views': total_views,
                   'comments': comments,
                   'comment_form': comment_form})


def ship_ranking(request):
    # get ship ranking dictionary
    ship_ranking = r.zrange('ship_ranking', 0, -1, desc=True)[:10]
    ship_ranking_ids = [int(id_) for id_ in ship_ranking]
    # get most viewed ship
    most_viewed = list(ShipList.objects.filter(id__in=ship_ranking_ids))
    most_viewed.sort(key=lambda x: ship_ranking_ids.index(x.id))
    return render(request,
                  'core/ranking.html',
                  {'most_viewed': most_viewed})


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
            # check if results contain only one ship
            if len(results) == 1:
                ship = [result.object.id for result in results][0]
                # get ship object or 404
                ship_object = get_object_or_404(ShipList, id=ship)
                # By passing object, get_absolute_url() method will be called to figure out the redirect URL
                return redirect(ship_object)
    return render(request,
                  'core/search.html',
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


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        # Form was submitted
        # Crated a form instance using submitted data
        form = ContactForm(request.POST)
        if form.is_valid():
            # TODO: reCAPTCHA passed validation
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            # Message body with name and email
            message = 'You have a message from {} ({}):\n\n{}'.format(form.cleaned_data['name'],
                                                                      form.cleaned_data['email'],
                                                                      form.cleaned_data['message'])
            try:
                send_mail(subject,
                          message,
                          from_email,
                          ['youremail@mail.com'],
                          fail_silently=False)
                messages.success(request, 'Thank you! Your email was sent and '
                                          'I will get back to you as soon as I can.')
                form = ContactForm()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

        else:
            messages.error(request, 'Oh snap! Better check yourself, change '
                                    'a few things up and try submitting again.')
    return render(request, 'core/contact.html', {'form': form})
