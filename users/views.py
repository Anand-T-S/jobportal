from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,TemplateView
from users.models import User
from users.forms import UserRegistrationForm,LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from users.decorators import signin_required


# Create your views here.

class SignUpView(CreateView):
    model = User
    template_name = "register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("signin")


class SignInView(FormView):
    model = User
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if not user:
                return render(request, "login.html", {"form":form})
            login(request, user)
            if request.user.is_candidate:
                return redirect("cand-home")
            else:
                return redirect("emp-home")


class HomeView(TemplateView):
    template_name = "home.html"


@signin_required
def sign_out(request, *args, **kwargs):
    logout(request)
    return redirect("signin")
