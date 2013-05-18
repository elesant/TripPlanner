from django.conf.urls import patterns, url


urlpatterns = patterns('core.views',
    url(r'^$', 'index'),
    url(r'^app/$', 'app'),
    url(r'^landing/$', 'view_landing'),
    url(r'^facebook-login/$', 'facebook_login'),
    url(r'^logout/$', 'logout'),
    url(r'^get_food$', 'get_food_recommendations'),
    url(r'^get_attractions$', 'get_attractions_recommendations'),
    url(r'^get_accomodations$', 'get_accomodations_recommendations'),
    url(r'^get_events$', 'get_events_recommendations'),
    url(r'^plan/(?P<plan_id>\d+)/$', 'view_plan'),
    url(r'^api/plan/list/$', 'api_plan_list'),
    url(r'^api/plan/add/$', 'api_plan_add'),
    url(r'^api/plan/update/$', 'api_plan_update'),
    url(r'^api/collaborator/add/$', 'api_collaborator_add'),
)
