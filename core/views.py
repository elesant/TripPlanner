import urllib
from core.utils.network import get_domain
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import auth
from core.decorators import ajax_endpoint
from django.views.decorators.csrf import csrf_exempt
from core.models import Plan, User, Event
from core.utils.yelp import make_yelp_request
from core.utils.airbnb import make_airbnb_request
from core.utils.eventbrite import make_eventbrite_request
from django.contrib.auth.decorators import login_required
from firebase import firebase
from summy import summy
import urllib2


def view_landing(request):
    context = RequestContext(request)
    return render_to_response('landing.html', context)


@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)


@login_required
def view_test(request):
    context = RequestContext(request)
    return render_to_response('test.html', context)


def facebook_login(request):
    login_link = 'https://www.facebook.com/dialog/oauth?' + urllib.urlencode(
        {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': get_domain(request) + '/',
            'response_type': 'code',
            'scope': 'email',
            'state': 'facebook',
        }
    )
    return HttpResponseRedirect(login_link)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def app(request):
    context = RequestContext(request)
    return render_to_response('app.html', context)


@login_required
def view_plan(request, plan_id=None):
    context = RequestContext(request)
    try:
        plan = Plan.objects.get(id=plan_id)
        context['plan'] = plan
    except Plan.DoesNotExist:
        raise Http404
    return render_to_response('plan.html', context)


@csrf_exempt
@ajax_endpoint
def api_link_summarize(request):
    link = request.POST['link']
    doc = urllib2.urlopen(link)
    response = summy.summarize(doc.read())
    return response, 200


@csrf_exempt
@login_required
@ajax_endpoint
def api_plan_list(request):
    response = {}
    plans = request.user.get_plans()
    response['plans'] = []
    for plan in plans:
        datum = {}
        datum['id'] = plan.id
        datum['title'] = plan.title
        response['plans'].append(datum)
    return response, 200


@csrf_exempt
@login_required
@ajax_endpoint
def api_plan_add(request):
    response = {}
    title = request.POST['title']
    new_plan = Plan(title=title)
    new_plan.save()
    new_plan.add_collaborator(request.user)
    response['plan_id'] = new_plan.id
    response['collaborator_id'] = request.user.id
    return response, 201


@csrf_exempt
@login_required
@ajax_endpoint
def api_plan_update(request):
    response = {}
    plan_id = request.POST['plan_id']
    title = request.POST['title']
    plan = Plan.objects.get(id=plan_id)
    plan.title = title
    plan.save()
    response['plan_id'] = plan.id
    response['collaborator_id'] = request.user.id
    return response, 200


@csrf_exempt
@login_required
@ajax_endpoint
def api_event_list(request):
    response = {}
    plan_id = request.POST['plan_id']
    plan = Plan.objects.get(id=plan_id)
    events = plan.get_events()
    response['events'] = []
    for event in events:
        datum = {}
        datum['id'] = event.id
        datum['header'] = event.header
        response['events'].append(datum)
    return response, 200


@csrf_exempt
@login_required
@ajax_endpoint
def api_event_add(request):
    response = {}
    header = request.POST['header']
    category = request.POST['category']
    plan_id = request.POST['plan_id']
    plan = Plan.objects.get(id=plan_id)
    new_event = Event()
    new_event.header = header
    new_event.category = category
    new_event.plan = plan
    new_event.order = len(plan.get_events())
    new_event.save()
    response['event_id'] = new_event.id
    response['collaborator_id'] = request.user.id
    return response, 201


@csrf_exempt
@login_required
@ajax_endpoint
def api_event_reorder(request):
    response = {}
    plan_id = request.POST['plan_id']
    plan = Plan.objects.get(id=plan_id)
    src_order = int(request.POST['src_order'])
    dest_order = int(request.POST['dest_order'])
    src_event = Event.objects.get(order=src_order, plan=plan)
    if src_order < dest_order:
      dec_events = Event.objects.filter(order__range=[src_order + 1, dest_order])
      for event in dec_events:
        event.order -= 1
        event.save()
      inc_events = Event.objects.filter(order__gt=dest_order)
      for event in inc_events:
        event.order += 1
        event.save()
    else:
      inc_events = Event.objects.filter(order__range=[dest_order, src_order - 1])
      print inc_events
      for event in inc_events:
        event.order += 1
        event.save()
      dec_events = Event.objects.filter(order__gt=src_order)
      print dec_events
      for event in dec_events:
        event.order -= 1
        event.save()
    src_event.order = dest_order
    src_event.save()
    return response, 200


@csrf_exempt
@login_required
@ajax_endpoint
def api_firebase_resync(request):
    response = {}
    if request.user.is_staff:
        fb_obj = firebase.FirebaseApplication('https://grouptrotter.firebaseio.com', None)
        plans = Plan.objects.all()
        for plan in plans:
            data = {
                'title': plan.title,
                'collaborators': [user.id for user in plan.get_collaborators()],
            }
            result = fb_obj.put('/plans', plan.id, data, connection=None)
            print result
        return response, 200
    else:
        return response, 403


@csrf_exempt
@login_required
@ajax_endpoint
def api_collaborator_add(request):
    response = {}
    plan_id = request.POST['plan_id']
    plan = Plan.objects.get(id=plan_id)
    if request.user in plan.get_collaborators():
        collaborator_id = request.POST.get('collaborator_id', request.user.id)
        collaborator = User.objects.get(id=collaborator_id)
        plan.add_collaborator(collaborator)
        response['plan_id'] = plan_id
        response['collaborator_id'] = collaborator_id
        return response, 201
    else:
        return response, 403

@csrf_exempt
@ajax_endpoint
def get_events_recommendations(request):
  url_params = {}
  # TODO add check-in, check-out, num_guests
  url_params['city'] = request.GET.get('address')
  num_results = 10
  response = make_eventbrite_request(url_params)
  return response, 200

@csrf_exempt
@ajax_endpoint
def get_accomodations_recommendations(request):
  url_params = {}
  # TODO add check-in, check-out, num_guests
  url_params['location'] = request.GET.get('address')
  num_results = 10
  response = make_airbnb_request(url_params).body
  return response, 200

@csrf_exempt
@ajax_endpoint
def get_attractions_recommendations(request):
  location = request.GET.get('address')
  num_results = 10
  url_params = {
    'term': 'major attractions',
    'location': location,
    'limit': num_results
  }
  response = make_yelp_request(url_params)
  return response, 200

@csrf_exempt
@ajax_endpoint
def get_food_recommendations(request):
  location = request.GET.get('address')
  num_results = 10
  url_params = {
    'term': 'food',
    'location': location,
    'limit': num_results
  }
  response = make_yelp_request(url_params)
  return response, 200
