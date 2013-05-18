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


@csrf_exempt
@ajax_endpoint
def test_endpoint(request):
    response = {}
    response['value'] = 12
    return response, 200

@csrf_exempt
@ajax_endpoint
def get_yelp_data(request):
  #address = request['address']
  consumer_key = 'wK9mRik-g9SFrrlRfvPAsQ'
  consumer_secret = 'hVvcWP5l4cuC8SpiaJrE7LpMIzQ'
  token = 'DFvHLSzfNqQDbsuLs-1T-zPk-mkZ0Z0d'
  token_secret = 'S4pO5Tn65qnP6JMq8Bi1XhDrcDk'
  url_params = {
    'term': 'bars',
    'location': 'sf',
    'limit': 10
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
