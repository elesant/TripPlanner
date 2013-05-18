from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
import urllib
from core.utils.network import get_domain
from django.conf import settings
from django.contrib import auth
from core.decorators import ajax_endpoint
from django.views.decorators.csrf import csrf_exempt
from core.models import Plan, User
from django.contrib.auth.decorators import login_required


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
    response['plan_id'] = new_plan.id
    response['collaborator_id'] = request.user.id
    return response, 201


@csrf_exempt
@login_required
@ajax_endpoint
def api_collaborator_add(request):
    response = {}
    plan_id = request.POST['plan_id']
    plan = Plan.objects.get(id=plan_id)
    print plan.get_collaborators()
    if request.user in plan.get_collaborators():
        collaborator_id = request.POST.get('collaborator_id', request.user.id)
        collaborator = User.objects.get(id=collaborator_id)
        plan.add_collaborator(collaborator)
        response['plan_id'] = plan_id
        response['collaborator_id'] = collaborator_id
        return response, 201
    else:
        return response, 403
