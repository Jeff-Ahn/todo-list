from rest_framework import status
from rest_framework.reverse import reverse
from server.common.api_test import CommonAPITestCase
from faker import Faker

fake = Faker()


class AccountAPITest(CommonAPITestCase):
    def test_create_account(self):
        signup_data = self._generate_valid_signup_data()
        response = self.client.post(reverse('account-list'),
                                    signup_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_valid_id_password(self):
        signup_data = self._generate_valid_signup_data()
        self.client.post(reverse('account-list'), signup_data, format='json')

        response = self.client.post(reverse('login'), {
            "email": signup_data["email"],
            "password": signup_data["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_id_password(self):
        signup_data = self._generate_valid_signup_data()
        self.client.post(reverse('account-list'), signup_data, format='json')
        response = self.client.post(reverse('login'), {
            "email": signup_data["email"],
            "password": "WRONG_PASSWORD"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        person = self.create_person_with_login()
        password = person.user.password
        response = self.client.patch(reverse('account-change-password'),
                                     {"password": "TEST_PASSWORD"},
                                     format='json')
        new_password = person.user.password
        self.assertNotEqual(password, new_password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _generate_valid_signup_data(self):
        return {
            "email": fake.safe_email(),
            "password": fake.password(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
