import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail


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

    def verify_email(self):
        if self.email_verified is False:   # 이미 이메일 검증되었다면
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            send_mail(
                "Verify Airbnb Account",
                f"Verify Account, this is your secret: {secret}",
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
            )
        return                              # 그냥 넘어감
