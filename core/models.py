from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """ Time Stamped model """

    created = models.DateField(auto_now_add=True)       # Model 이 생성된 날짜
    updated = models.DateField(auto_now=True)           # 새로운 날짜 업데이트

    class Meta:
        abstract = True
