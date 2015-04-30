from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import praw
import json


class IndexView(TemplateView):
    template_name = 'index.html'


def init_praw(access_credentials=None):
    r = praw.Reddit('Doing oauth testing by /u/godlikesme')
    r.set_oauth_app_info(settings.REDDIT_APP_ID, settings.REDDIT_APP_SECRET, settings.REDDIT_AUTH_REDIRECT_URI)
    if access_credentials:
        r.set_access_credentials(**access_credentials)
    return r


def AuthView(request):
    r = init_praw()
    auth_link = r.get_authorize_url('UniqueKey', 'mysubreddits,identity,flair')
    return HttpResponseRedirect(auth_link)


def serialize_reddit_access_information(ai):
    serializable_ai = {"access_token": ai['access_token'],
                       "refresh_token": ai['refresh_token'],
                       "scope": list(ai['scope'])}
    return json.dumps(serializable_ai)


def deserialize_reddit_access_information(serialized_ai):
    serializable_ai = json.loads(serialized_ai)
    ai = serializable_ai
    ai['scope'] = set(serializable_ai['scope'])
    return ai


def AuthCallbackView(request):
    r = init_praw()

    code = request.GET.get('code', '')
    ai = r.get_access_information(code)

    response = HttpResponseRedirect(reverse("results"))
    response.set_cookie('ai', serialize_reddit_access_information(ai))

    return response


def GetFlairView(request, subreddit):
    try:
        r = init_praw(deserialize_reddit_access_information(request.COOKIES.get('ai', '')))
    except:
        return HttpResponse(json.dumps({"login_again": True}), content_type='application/json')
    flair_text = r.get_flair_choices(subreddit)['current']['flair_text']

    return HttpResponse(json.dumps({"subreddit": subreddit, "flair": flair_text if flair_text else None}), content_type='application/json')


def GetMySubredditsView(request):
    try:
        r = init_praw(deserialize_reddit_access_information(request.COOKIES.get('ai', '')))
    except:
        return HttpResponse(json.dumps({"login_again": True}), content_type='application/json')
    subreddits = [sr.url[3:][:-1] for sr in r.get_my_subreddits(limit=1000)]
    return HttpResponse(json.dumps({"subreddits": subreddits}), content_type='application/json')


class ResultsView(TemplateView):
    template_name = 'results.html'
