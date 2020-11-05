from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


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

    avatar = models.ImageField(blank=True)                     # 프로필사진
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10,  blank=True)    # 성별   10자, null 허용
    bio = models.TextField(blank=True)  # 바이오그래피 - 간략 소개
    birthdate = models.DateField(blank=True, null=True)         # 생일
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2,  blank=True)    # 언어
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3,  blank=True)    # 환율,통화 (화폐)
    superhost = models.BooleanField(default=False)  # 슈퍼유저 여부
