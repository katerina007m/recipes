from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .models import Profile, CustomUserCreationForm


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

    def get(self, request, *args, **kwargs):
        if request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {},
                status=200,
            )

        return super().get(request, *args, **kwargs)


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

        if self.request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "success": True,
                    "message": "User registered successfully.",
                    "user": {
                        "id": self.object.id,
                        "username": self.object.username,
                        "email": self.object.email,
                    },
                },
                status=201,
            )

        return response

    def form_invalid(self, form):
        # Handle form errors
        if self.request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "success": False,
                    "errors": form.errors,
                    "message": "Invalid data submitted.",
                },
                status=400,
            )

        # Default to rendering the form again for non-JSON requests
        return super().form_invalid(form)


class MyLoginView(LoginView):
    template_name = "myauth/login.html"

    def form_valid(self, form):
        html_response = super().form_valid(form)
        if self.request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "success": True,
                    "message": "User logged in successfully.",
                    "user": {
                        "id": self.request.user.id,
                        "username": self.request.user.username,
                        "csrf_token": self.request.META.get("CSRF_COOKIE"),
                    },
                },
                status=200,
            )
        return html_response

    def form_invalid(self, form):
        html_response = super().form_valid(form)
        if self.request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "success": False,
                    "errors": form.errors,
                    "message": "Invalid data submitted.",
                },
                status=400,
            )
        return html_response


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)

    if request.headers.get("Accept") == "application/json":
        return JsonResponse(
            {
                "success": True,
                "message": "User logged out successfully.",
            },
            status=200,
        )

    return redirect("myauth:login")
