from datetime import datetime, timedelta
from random import choice, choices, randint, random

from locust import FastHttpUser, task, constant_pacing

regions = [
    "5d08e36dad3a9a001701b95f", "5d08e36dad3a9a001701b960", "5d08e36dad3a9a001701b95c", "5d08e36dad3a9a001701b963",
    "5d08e36dad3a9a001701b951", "5d08e36dad3a9a001701b961", "5d08e36fad3a9a001701b9d4", "5d08e36fad3a9a001701b9d2",
    "5d08e36fad3a9a001701b9c5", "5d08e36fad3a9a001701b9d5", "5d08e36dad3a9a001701b964", "5d08e36fad3a9a001701b9d0",
    "5d08e36fad3a9a001701b9d1", "5d08e36dad3a9a001701b97c", "5d08e36dad3a9a001701b96b", "5d08e36dad3a9a001701b965",
    "5d08e36dad3a9a001701b968", "5d08e36dad3a9a001701b970", "5d08e36dad3a9a001701b978", "5d08e36dad3a9a001701b972",
    "5d08e36dad3a9a001701b96a", "5d08e36dad3a9a001701b96d", "5d08e36dad3a9a001701b976", "5d08e36dad3a9a001701b96e",
    "5d08e36dad3a9a001701b977", "5dd464abb3d9ab0012402632", "5d08e36dad3a9a001701b96c", "5d08e36dad3a9a001701b96f",
    "5d08e36dad3a9a001701b97a", "5d08e36dad3a9a001701b979", "5d08e36dad3a9a001701b97b", "5d08e36dad3a9a001701b975",
    "5d08e36dad3a9a001701b95b", "5d08e36dad3a9a001701b974", "5d08e36ead3a9a001701b97f", "5d08e36dad3a9a001701b973",
    "5d08e36ead3a9a001701b981", "5fb25cf85e7ea700188ddc8b", "5d08e36ead3a9a001701b980", "5d08e36dad3a9a001701b97d",
    "5d08e36dad3a9a001701b97e", "5d08e36dad3a9a001701b958", "5d08e36dad3a9a001701b94b", "5d08e36dad3a9a001701b952",
    "5d08e36dad3a9a001701b949", "5d08e36dad3a9a001701b94d", "5d08e36dad3a9a001701b94a", "5d08e36dad3a9a001701b953",
    "5d08e36dad3a9a001701b946", "5d08e36dad3a9a001701b947", "5d08e36dad3a9a001701b94e", "5d08e36dad3a9a001701b948",
    "5d08e36dad3a9a001701b95a", "5d08e36dad3a9a001701b955", "5d08e36dad3a9a001701b954", "5d08e36dad3a9a001701b94f",
    "5d08e36dad3a9a001701b957", "5d08e36dad3a9a001701b959", "5d08e36dad3a9a001701b950", "5d08e36dad3a9a001701b95d",
    "5d08e36dad3a9a001701b956", "5d08e36fad3a9a001701b9c7", "5d08e36fad3a9a001701b9bf", "5d08e36fad3a9a001701b9c3",
    "5d08e36fad3a9a001701b9c8", "5d08e36dad3a9a001701b94c", "5d08e36fad3a9a001701b9c1", "608bb152f83b4e0019348391",
    "5d08e36fad3a9a001701b9c6", "5d08e36fad3a9a001701b9ca", "5d08e36fad3a9a001701b9c9", "5d08e36fad3a9a001701b9cf",
    "5d08e36fad3a9a001701b9cb", "5d08e36fad3a9a001701b9cc", "5d08e36fad3a9a001701b9c0", "5d08e36fad3a9a001701b9cd",
    "5d08e36fad3a9a001701b9ce", "5d08e36fad3a9a001701b9d3", "5d08e36dad3a9a001701b966", "5d08e36dad3a9a001701b962",
    "5d08e36dad3a9a001701b967", "5d08e36dad3a9a001701b95e", "5d08e36fad3a9a001701b9c2", "5d08e36fad3a9a001701b9c4",
    "5d08e36dad3a9a001701b969",
]


def random_birthday() -> str:
    start = datetime.now() - timedelta(days=365*100)
    end = datetime.now() - timedelta(days=365*10)
    birthday = start + (end - start) * random()
    return birthday.isoformat()


class GetQuestionnaireUser(FastHttpUser):
    wait_time = constant_pacing(1)
    @task
    def get_questionnaire(self):
        self.client.get(
            url="/questionnaire",
            params={"email": "locust@mail.ru"},
        )


class PostQuestionnaireUser(FastHttpUser):
    wait_time = constant_pacing(1)
    @task
    def post_questionnaire(self):
        data = {
            "birthday_at": random_birthday(),
            "sex": choice(("male", "female")),
            "family_status": choice(("married", "in_relationship", "single")),
            "has_children_below_18": choice((False, True)),
            "tourism_goals": choices(population=("active", "calm", "cultural", "social"), k=randint(1, 4)),
            "region": choice(regions)
        }
        self.client.post(
            url="/questionnaire",
            params={"email": "locust@mail.ru"},
            json=data
        )


class PopularRecommendationUser(FastHttpUser):
    wait_time = constant_pacing(1)
    @task
    def get_popular(self):
        self.client.get(
            url="/recommendation/popular",
            params={
                "email": "locust@mail.ru",
                "object_type": choice(("event", "excursion", "hotel", "place", "restaurant", "route", "tour", "track"))
            },
        )


class UserBasedRecommendationUser(FastHttpUser):
    wait_time = constant_pacing(1)

    @task
    def get_user_based(self):
        self.client.get(
            url="/recommendation/user_based",
            params={
                "email": "locust@mail.ru",
                "object_type": choice(("event", "excursion", "hotel", "place", "restaurant", "route", "tour", "track"))
            },
        )
