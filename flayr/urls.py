from django.conf.urls import include, url
from django.contrib import admin
from .views import IndexView, AuthView, AuthCallbackView

urlpatterns = [
    # Examples:
    # url(r'^$', 'flayr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^auth$', AuthView.as_view(), name='auth'),
    url(r'^authorize_callback', AuthCallbackView.as_view(), name='auth_callback'),
]
