import os
import requests
from django.forms.forms import Form
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# 14.4
# class LoginView(View):

#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "hho3999@naver.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})

# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))


# 14.5

class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # lazy : view 가 필요로할 때 호출 > 바로 실행하지 않음
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Hwang",
        "last_name": "Hyeonho",
        "email": "hemail@naver.com",
    }

    # 회원가입 후 바로 로그인 되도록 설정
    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        user.verify_email()         # 유저 로그인 되면 verificatino 보냄
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # 이메일코드 안보이도록 공백 설정
        user.save()
        # to do : add success message
    except models.User.DoesNotExist:
        # to do : add erroe message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                                          headers={
                                              "Accept": "application/json"},
                                          )
            token_json = token_request.json()
            error = token_json.get("error", None)
            # json 에러 판별
            if error is not None:
                return redirect(reverse("users:login"))
            else:
                # json 에러 없다면 토큰을 가져 옴
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json"
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get('login', None)
                if username is not None:                    # user 가 존재한다면
                    # name = profile_json.get('name')
                    # bio = profile_json.get('bio')
                    email = profile_json.get('email')
                    name = profile_json.get("name")
                    name = username if name is None else name   # 없다면 username
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio        # 없다면 공백
                    try:
                        user = models.User.objects.get(
                            email=email)     # 같다면 이미 로그인 되어있음 의미
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:    # user 존재하지 않을 경우
                        user = models.User.objects.create(  # 새 유저 생성!
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        # 아래부터 깃헙으로 로그인해주는 코드
                        user.set_unusable_password()    # 어떠한 pw도 적용되지 않음
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))
