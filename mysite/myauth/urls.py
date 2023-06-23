from django.urls import path
from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
)
from django.contrib.auth.views import LoginView


app_name = 'myauth'

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"),
    path("logaut/", MyLogoutView.as_view(), name="logaut"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),
]
