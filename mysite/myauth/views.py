from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .models import Profile, CustomUserCreationForm


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(
            user=self.object,
            bio=form.cleaned_data.get("bio", ""),
        )
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        if user:
            login(request=self.request, user=user)
        return response


class MyLoginView(LoginView):
    template_name = "myauth/login.html"


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("myauth:login")
