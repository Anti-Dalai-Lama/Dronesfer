from django.shortcuts import render
from .forms import UserForm, LoginForm, CreateRouteForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Route, Location, Drone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def welcome(request):
    r = request
    if request.user.is_authenticated:
        return routes(request)
    else:
        return render(request, 'welcome.html')

@login_required()
def routes(request):
    user = User.objects.filter(username=request.user.username)
    all_routes = Route.objects.filter(customer=user)
    return render(request, 'routes.html', {'all_routes': all_routes})

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


def detail(request, route_id):
    route = get_object_or_404(Route, pk=route_id)
    return render(request, "detail.html", {"route": route})


class CreateRouteFormView(View):
    form_class = CreateRouteForm
    template_name = 'create_route.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            pass

        return render(request, self.template_name, {'form': form})