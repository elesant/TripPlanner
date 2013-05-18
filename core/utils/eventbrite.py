import unirest
import urllib
from django.conf import settings

def make_eventbrite_request(url_params):
  encoded_params = ''
  url_params.update({'app_key': settings.EVENTBRITE_API_CONSTANTS['APP_KEY']})
  encoded_params = urllib.urlencode(url_params)

  url = "%s?%s" % (
    settings.EVENTBRITE_API_CONSTANTS['HOST'],
    encoded_params
  )
  print url
  return unirest.get(url).body
