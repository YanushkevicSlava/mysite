from django.http import HttpRequest
import time
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):

    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exceptions_count = 0
        # self.request_time = {}
        self.request_ip = {}

    def __call__(self, request: HttpRequest):
        time_rest = 1
        if not self.request_ip:
            print("This is first request after runserver")
        else:
            if (round(time.time()) * 1) - self.request_ip[request.META.get("REMOTE_ADDR")] < time_rest:
                return render(request, 'requestdataapp/error-time-request.html')

        self.request_ip[request.META.get("REMOTE_ADDR")] = (round(time.time()) * 1)
        #     if (round(time.time()) * 1) - self.request_time["time"] < time_rest \
        #          and self.request_ip["ip_address"] == request.META.get("REMOTE_ADDR"):
        #         print("It's been less than 10 seconds since your last request!")
        #         return render(request, 'requestdataapp/error-time-request.html')
        #
        # self.request_time = {
        #     "time": (round(time.time()) * 1),
        #     }
        # self.request_ip = {
        #     "ip_address": request.META.get("REMOTE_ADDR")
        # }

        self.request_count += 1
        print("request count", self.request_count)
        response = self.get_response(request)
        self.response_count += 1
        print("response count", self.response_count)
        return response

    def process_exceptions(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions far")



