from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView, AuthView, AuthCallbackView, ResultsView, GetFlairView, GetMySubredditsView

urlpatterns = [
    # Examples:
    # url(r'^$', 'flayr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^auth$', AuthView, name='auth'),
    url(r'^authorize_callback', AuthCallbackView, name='auth_callback'),
    url(r'^results', ResultsView.as_view(), name='results'),
    url(r'^_get_flair/([^/]+)$', GetFlairView, name='_get_flair'),
    url(r'^_get_my_subreddits$', GetMySubredditsView, name='_get_my_subreddits'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
