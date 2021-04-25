from rest_framework import status
from server.common.api_test import CommonAPITestCase
from rest_framework.reverse import reverse
from faker import Faker
import json

fake = Faker()


class TodoAPITest(CommonAPITestCase):
    def setUp(self) -> None:
        self.person = self.create_person_with_login()

    def test_create_todo(self):
        new_todo = self._generate_valid_random_todo()
        response = self.client.post(reverse('todo-list'),
                                    new_todo,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_todo(self):
        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo(self):
        new_todo = self._generate_valid_random_todo()
        response = self.client.post(reverse('todo-list'),
                                    new_todo,
                                    format='json')

        current_todo = response.data
        response = self.client.put(reverse('todo-detail',
                                           kwargs={'pk': current_todo['id']}),
                                   data={
                                       "content": "NEW_CONTENT",
                                       "is_done": True
                                   },
                                   format='json')
        current_todo = json.dumps(current_todo)
        updated_todo = json.dumps(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONNotEqual(current_todo, updated_todo)

    def test_delete_todo(self):
        new_todo = self._generate_valid_random_todo()
        response = self.client.post(reverse('todo-list'),
                                    new_todo,
                                    format='json')
        current_todo = response.data
        response = self.client.delete(
            reverse('todo-detail', kwargs={'pk': current_todo['id']}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def _generate_valid_random_todo(self):
        return {"content": fake.paragraph(nb_sentences=5), "is_done": False}
