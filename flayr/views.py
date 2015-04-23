from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import praw


class IndexView(TemplateView):
    template_name = 'index.html'


class AuthView(TemplateView):
    def get(self, request, *args, **kwargs):
        r = praw.Reddit('Doing oauth testing by /u/godlikesme')
        r.set_oauth_app_info(settings.REDDIT_APP_ID, settings.REDDIT_APP_SECRET, settings.REDDIT_AUTH_REDIRECT_URI)
        auth_link = r.get_authorize_url('UniqueKey')
        return HttpResponseRedirect(auth_link)


class AuthCallbackView(TemplateView):
    def get(self, request, *args, **kwargs):
        r = praw.Reddit('Doing oauth testing by /u/godlikesme')
        r.set_oauth_app_info(settings.REDDIT_APP_ID, settings.REDDIT_APP_SECRET, settings.REDDIT_AUTH_REDIRECT_URI)

        state = request.GET.get('state', '')
        code = request.GET.get('code', '')
        info = r.get_access_information(code)
        user = r.get_me()
        variables_text = "State=%s, code=%s, info=%s." % (state, code,
                                                          str(info))
        text = 'You are %s and have %u link karma.' % (user.name,
                                                       user.link_karma)
        return HttpResponse(variables_text + '</br></br>' + text)
