from rest_framework import status
from server.common.api_test import CommonAPITestCase
from rest_framework.reverse import reverse
from faker import Faker
import json

fake = Faker()


class TodoAPITest(CommonAPITestCase):
    def setUp(self) -> None:
        self.person = self.create_person_with_login()
        self.todo = self._generate_valid_random_todo()
        self.response = self.client.post(reverse('todo-list'),
                                         self.todo,
                                         format='json')

    def test__create_todo__when__valid_request__expect__201_created(self):
        new_todo = self._generate_valid_random_todo()
        response = self.client.post(reverse('todo-list'),
                                    new_todo,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test__get_todo__when__valid_request__expect__200_ok(self):
        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test__update_todo_when__valid_request__expect__200_ok(self):
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

    def test__delete_todo_when__valid_request__expect__204_no_content(self):
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
