from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from .models import ShipList, Comment
from .forms import SearchForm, ContactForm, CommentForm

import json
import urllib
from haystack.query import SearchQuerySet
import redis
from django.conf import settings

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def ship_detail(request, ship):
    # get ship object
    ship = get_object_or_404(ShipList, slug=ship)
    # increment total ship views by 1
    total_views = r.incr('ship:{}:views'.format(ship.id))
    # ship ranking increment by 1
    r.zincrby('ship_ranking', ship.id, 1)
    # list of active parent comments
    comments = ship.comments.filter(active=True, parent__isnull=True)
    if request.method == 'POST':
        # comment has been added
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # if parent_id = None - proceed with normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            new_comment.ship = ship
            # save
            new_comment.save()
            messages.success(request, 'Your comment has been submitted.')
            return HttpResponseRedirect(ship.get_absolute_url())
        else:
            messages.error(request, 'Oh snap! Better check yourself, change '
                                    'a few things up and try submitting again.')
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
    ship_ranking = r.zrange('ship_ranking', 0, -1, desc=True)[:15]
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
    # autocomplete for ships name
    sqs1 = SearchQuerySet().autocomplete(text=query)[:7]
    # autocomplete for country
    sqs2 = SearchQuerySet().autocomplete(country_auto=query)
    # create list of suggested ships
    suggestions_ship = [result.object.ship for result in sqs1]
    # create a list with suggested country
    suggestions_country = list(set([result.object.country for result in sqs2]))
    # combine two lists of suggestions
    results = suggestions_ship + suggestions_country
    # Make sure you return a JSON object, not a bare list.
    # if other than dict you must set the safe parameter to False
    return JsonResponse(results, safe=False)


def contact(request):
    """Contact view is responsible for rendering contact form. After
    submission function checks if form pass reCAPTCHA validation. If form
    pass validation function creates a message object and send it or display
    error message for the user.
    """
    if request.method == 'GET':
        form = ContactForm()
    else:
        # Form was submitted
        # Crated a form instance using submitted data
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            # Begin reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # End reCAPTCHA validation
            if result['success']:
                # reCAPTCHA passed validation
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
                    return redirect('core:contact')
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

            else:
                messages.error(request, 'Oh snap! Better check yourself, change '
                                        'a few things up and try submitting again.')
    return render(request, 'core/contact.html', {'form': form})


def about(request):
    return render(request, 'core/about.html')
