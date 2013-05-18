import unirest
import urllib
from django.conf import settings

def make_airbnb_request(url_params):
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)

  url = "%s?%s" % (
    settings.AIRBNB_API_CONSTANTS['HOST'],
    encoded_params
  )

  response = unirest.get(url,
    {
      "X-Mashape-Authorization": "K5X98rffrPcDDxTBgHuCv2Hqko7eGQAa"
    });
  return response
