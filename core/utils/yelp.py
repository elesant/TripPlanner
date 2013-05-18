import urllib
import urllib2
import json
import oauth2
from django.conf import settings

def make_yelp_request(url_params):
  """Returns response for API request."""
  token = settings.YELP_API_CONSTANTS['TOKEN']
  consumer_key = settings.YELP_API_CONSTANTS['CONSUMER_KEY']
  token_secret = settings.YELP_API_CONSTANTS['TOKEN_SECRET']
  consumer_secret = settings.YELP_API_CONSTANTS['CONSUMER_SECRET']
  host = settings.YELP_API_CONSTANTS['HOST']
  path = settings.YELP_API_CONSTANTS['PATH']

  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  #print 'URL: %s' % (url,)

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
  #print 'Signed URL: %s\n' % (signed_url,)

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

