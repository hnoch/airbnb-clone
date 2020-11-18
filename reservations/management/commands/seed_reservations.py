import random
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

NAME = "reservations"


class Command(BaseCommand):
    help = "This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many {NAME} do you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "room": lambda x: random.choice(rooms),
                "guest": lambda x: random.choice(users),
                "check_in": lambda x: datetime.now(),           # 체크인 = 현재를 기준으로 설정
                # 체크아웃 = 현재날짜로부터 3~25사이의 시간을 더해 설정
                "check_out": lambda x: datetime.now() + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
