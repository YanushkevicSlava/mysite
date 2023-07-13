from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, \
    user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from .models import Profile
from .forms import ProfileEditForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


class UsersListView(ListView):
    model = User
    template_name = "myauth/users-list.html"
    context_object_name = "users"


class ProfileUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.is_staff

    model = Profile
    form_class = ProfileEditForm

    def get_success_url(self):
        return reverse(
            "myauth:about-me",
            kwargs={"pk": self.object.pk},
        )



