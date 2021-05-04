from rest_framework.test import APITestCase
from server.account.models import Person
from .test import create_person


class CommonAPITestCase(APITestCase):
    def create_person_with_login(self) -> Person:
        person = create_person()
        self.force_login(person)

        return person

    def force_login(self, person: Person):
        user = person.user

        self.client.force_authenticate(user=user)
