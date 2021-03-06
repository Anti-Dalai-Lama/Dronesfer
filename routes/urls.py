from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'routes'

urlpatterns = [
    #/routes/
    url(r'^$', views.routes, name="routes"),

    #/routes/detail/id
    url(r'^detail/(?P<route_id>[0-9]+)/$', views.detail, name="detail"),

    #/routes/delete/id
    url(r'^delete/(?P<route_id>[0-9]+)/$', views.delete, name="delete"),

    #/routes/create
    url(r'^create/$', login_required(views.CreateRouteFormView.as_view()), name="create"),

    #/routes/create
    url(r'^update/(?P<route_id>[0-9]+)/$', login_required(views.UpdateRouteFormView.as_view()), name="update"),

    #/routes/view/id
    #url(r'^view/(?P<route_id>[0-9]+)/$', views.DetailView.as_view(), name="detail"),

]