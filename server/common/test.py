from faker import Faker
from server.account.models import User, Person

fake = Faker()


def create_person() -> Person:
    user = User.objects.create(email=fake.safe_email(),
                               password=fake.password())
    person = Person.objects.create(
        user=user,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )

    return person
