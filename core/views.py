import urllib
import urllib2
import json
import oauth2

from core.utils.network import get_domain
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib import auth
from core.decorators import ajax_endpoint
from django.views.decorators.csrf import csrf_exempt
from core.models import Plan, User
from django.contrib.auth.decorators import login_required
from firebase import firebase


def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)


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


def app(request):
    context = RequestContext(request)
    return render_to_response('app.html', context)


@csrf_exempt
@login_required
@ajax_endpoint
def api_plan_add(request):
    response = {}
    title = request.POST['title']
    new_plan = Plan(title=title)
    new_plan.save()
    new_plan.add_collaborator(request.user)
    fb_obj = firebase.FirebaseApplication('https://grouptrotter.firebaseio.com', None)
    plan_url = '/plans'
    data = {
        'title': new_plan.title,
        'collaborators': [user.id for user in new_plan.get_collaborators()],
    }
    result = fb_obj.put(plan_url, new_plan.id, data, connection=None)
    response['plan_id'] = new_plan.id
    response['collaborator_id'] = request.user.id
    response['firebase_result'] = result
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
    fb_obj = firebase.FirebaseApplication('https://grouptrotter.firebaseio.com', None)
    plan_url = '/plans/%s' % plan.id
    data = {
        'title': plan.title,
    }
    result = fb_obj.patch(plan_url, data, connection=None)
    response['plan_id'] = plan.id
    response['collaborator_id'] = request.user.id
    response['firebase_result'] = result
    return response, 200


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
        fb_obj = firebase.FirebaseApplication('https://grouptrotter.firebaseio.com', None)
        plan_url = '/plans/%s' % plan.id
        data = {
            'collaborators': [user.id for user in plan.get_collaborators()],
        }
        result = fb_obj.patch(plan_url, data, connection=None)
        response['plan_id'] = plan_id
        response['collaborator_id'] = collaborator_id
        response['firebase_result'] = result
        return response, 201
    else:
        return response, 403


@csrf_exempt
@ajax_endpoint
def get_yelp_data(request):
  location = request.GET.get('address')
  num_results = 10
  consumer_key = 'wK9mRik-g9SFrrlRfvPAsQ'
  consumer_secret = 'hVvcWP5l4cuC8SpiaJrE7LpMIzQ'
  token = 'DFvHLSzfNqQDbsuLs-1T-zPk-mkZ0Z0d'
  token_secret = 'S4pO5Tn65qnP6JMq8Bi1XhDrcDk'
  url_params = {
    'term': 'food',
    'location': location,
    'limit': num_results
  }
  response = make_yelp_request('api.yelp.com', '/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
  return response, 200


def make_yelp_request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
  print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response
