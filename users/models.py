import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):

    # 파이썬 표준 형식 - 무슨 클래스인지
    """ Custom User Model ** """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other")
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        # language_eng = db 저장될 값 / English = form에 보여질 값
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean")
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW")
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(
        upload_to="avatars", blank=True)                     # 프로필사진
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10,  blank=True)    # 성별   10자, null 허용
    bio = models.TextField(blank=True)  # 바이오그래피 - 간략 소개
    birthdate = models.DateField(blank=True, null=True)         # 생일
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2,  blank=True, default=LANGUAGE_KOREAN)    # 언어
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3,  blank=True, default=CURRENCY_KRW)    # 환율,통화 (화폐)
    superhost = models.BooleanField(default=False)  # 슈퍼유저 여부
    email_verified = models.BooleanField(default=False)    # 이메일 확인여부
    email_secret = models.CharField(
        max_length=20, default="", blank=True)  # 이메일 확인코드
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)  # 로그인 방식

    def verify_email(self):
        if self.email_verified is False:   # 이미 이메일 검증되었다면
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            # html_message = f'To verify your account click <a href="http://127.0.0.1/8000/users/verify/{secret}">here</a>'
            html_message = render_to_string(
                "emails/verify_email.html", {'secret': secret})
            send_mail(      # 실제 이메일을 보내는 항목
                "Verify Airbnb Account",            # 제목 칸
                # 메세지 칸 > (strip : html 가져다가 text로 변환)
                strip_tags(html_message),
                settings.EMAIL_FROM,        # 보내는 사람
                [self.email],               # 받는 사람 (여러개 포함-리스트)
                fail_silently=False,        # 에러 표시 여부
                html_message=html_message,  # html 링크로 표시
            )
            self.save()             # email_serect 저장
        return                              # 그냥 넘어감
