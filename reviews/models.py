from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()             # 리뷰텍스트
    accuracy = models.IntegerField()        # 정확성
    communication = models.IntegerField()   # 의사소통
    cleanliness = models.IntegerField()     # 꺠끗함
    location = models.IntegerField()        # 위치
    check_in = models.IntegerField()        # 체크인
    value = models.IntegerField()           # 가치
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):              # 리뷰 목록에 리뷰텍스트의 값이 보임(설정 안할 시 reveiw object(n))
        # return self.review
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)        # 둘쨰자리까지 반올림

    rating_average.short_description = "Avg."   # 상위필터 이름 설정
