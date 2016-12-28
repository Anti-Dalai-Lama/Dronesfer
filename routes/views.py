from django.shortcuts import render
from .forms import UserForm, LoginForm, CreateRouteForm, UpdateRouteForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Route, Location, Drone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import pytz

def welcome(request):
    r = request
    if request.user.is_authenticated:
        return routes(request)
    else:
        return render(request, 'welcome.html')

@login_required()
def routes(request):
    user = User.objects.filter(username=request.user.username)
    future_routes = Route.objects.filter(customer=user, time__gt=timezone.now()).order_by('time')
    past_routes = Route.objects.filter(customer=user, time__lte=timezone.now()).order_by('-time')
    return render(request, 'routes.html', {'future_routes': future_routes, 'past_routes': past_routes})

@login_required
def logout_user(request):
    logout(request)
    return render(request, 'welcome.html')

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('routes:routes')

        return render(request, self.template_name, {'form': form})

class LoginView(View):
    form_class = LoginForm
    template_name = 'login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('routes:routes')
        else:
            return render(request, self.template_name, {'form': self.form_class(None)})

@login_required()
def detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    is_future = None
    if(route.time > timezone.now()):
        is_future = True
    return render(request, "detail.html", {"route": route, 'is_future':is_future})

@login_required()
def delete(request, route_id):
    Route.objects.filter(id = route_id).delete()
    return routes(request)

class CreateRouteFormView(View):
    form_class = CreateRouteForm
    template_name = 'create_route.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            l_t = form.data['load_title']
            l_w = Decimal(form.data['load_weight'])
            cust = User.objects.filter(username=request.user.username)[0]
            dt = datetime.strptime(form.data['time'], '%H:%M %d.%m.%Y')
            dist = int(form.data['distance'])
            pr = Decimal(form.data['price'])
            drs = Drone.objects.all()
            dr = None
            diff = Decimal(10000)
            for drone in drs:
                if drone.add_weight >= l_w and drone.add_weight - l_w < diff:
                    dr = drone
                    diff = drone.add_weight - l_w


            # drone
            sp = form.data['start_point'].split('&')
            ep = form.data['end_point'].split('&')

            error_text = None
            comp_dt = pytz.timezone(timezone.get_default_timezone_name()).localize(dt)

            if comp_dt < (timezone.now() + timedelta(minutes=45)):
                error_text = "We can't do it so early"

            if dr == None:
                error_text = "Your load is too heavy to handle it"

            if error_text != None:
                return render(request, self.template_name,
                              {'form': form, 'error_message': error_text,
                               'start_lat': float(sp[1]), 'start_lng': float(sp[2]),
                               'end_lat': float(ep[1]), 'end_lng': float(ep[2])})

            s_l = Location(title=sp[0], latitude=float(sp[1]), longitude=float(sp[2]))
            s_l.save()
            e_l = Location(title=ep[0], latitude=float(ep[1]), longitude=float(ep[2]))
            e_l.save()

            delta = int(dist/dr.speed)
            end_t = dt + timedelta(seconds=delta)

            new_route = Route(load_title=l_t, load_weight=l_w, drone=dr, customer=cust, time=dt, end_time=end_t, distance=dist, start_point=s_l, end_point=e_l, price=pr)
            new_route.save()

            return redirect('routes:routes')

        sp = form.data['start_point'].split('&')
        ep = form.data['end_point'].split('&')
        return render(request, self.template_name, {'form': form, 'start_lat': float(sp[1]), 'start_lng': float(sp[2]), 'end_lat': float(ep[1]), 'end_lng': float(ep[2])})


class UpdateRouteFormView(View):
    form_class = UpdateRouteForm
    template_name = 'update_route.html'

    def get(self, request, route_id):
        route = Route.objects.filter(id=route_id)[0]
        form = self.form_class(initial={'load_title': route.load_title, 'load_weight': route.load_weight, 'time': route.time})
        return render(request, self.template_name, {'form': form, 'start_lat': route.start_point.latitude, 'start_lng': route.start_point.longitude,
                                                    'end_lat': route.end_point.latitude, 'end_lng': route.end_point.longitude})

    def post(self, request, route_id):
        form = self.form_class(request.POST)

        if form.is_valid():
            l_t = form.data['load_title']
            l_w = Decimal(form.data['load_weight'])
            dt = datetime.strptime(form.data['time'], '%H:%M %d.%m.%Y')


            dist = int(form.data['distance'])
            pr = Decimal(form.data['price'])
            drs = Drone.objects.all()
            dr = None
            diff = Decimal(10000)
            for drone in drs:
                if drone.add_weight >= l_w and drone.add_weight - l_w < diff:
                    dr = drone
                    diff = drone.add_weight - l_w

            sp = form.data['start_point'].split('&')
            ep = form.data['end_point'].split('&')

            error_text = None
            comp_dt = pytz.timezone(timezone.get_default_timezone_name()).localize(dt)
            if comp_dt < (timezone.now() + timedelta(minutes=45)):
                error_text = "We can't do it so early"

            if dr == None:
                error_text = "Your load is too heavy to handle it"

            if error_text != None:
                return render(request, self.template_name,
                              {'form': form, 'error_message': error_text,
                               'start_lat': float(sp[1]), 'start_lng': float(sp[2]),
                               'end_lat': float(ep[1]), 'end_lng': float(ep[2])})

            route = Route.objects.filter(id=route_id)[0]
            s_l = route.start_point
            s_l.title = sp[0]
            s_l.latitude = float(sp[1])
            s_l.longitude = float(sp[2])
            s_l.save()
            e_l = Route.objects.filter(id=route_id)[0].end_point
            e_l.title = ep[0]
            e_l.latitude = float(ep[1])
            e_l.longitude = float(ep[2])
            e_l.save()

            delta = int(dist / dr.speed)
            end_t = dt + timedelta(seconds=delta)

            route.load_title = l_t
            route.load_weight = l_w
            route.drone = dr
            route.time = dt
            route.end_time = end_t
            route.distance = dist
            route.price = pr
            route.save()

            return redirect('routes:routes')

        sp = form.data['start_point'].split('&')
        ep = form.data['end_point'].split('&')
        return render(request, self.template_name, {'form': form, 'start_lat': float(sp[1]), 'start_lng': float(sp[2]), 'end_lat': float(ep[1]), 'end_lng': float(ep[2])})

