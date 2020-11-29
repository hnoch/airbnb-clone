from django.forms.forms import Form
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms

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
