from rest_framework import status
from server.common.api_test import CommonAPITestCase
from server.todo.models import Todo
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
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)

    def test__get_todo__when__valid_request__expect__200_ok(self):
        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.count(), 1)

    def test__update_todo_when__valid_request__expect__200_ok(self):
        todo = Todo.objects.get()
        response = self.client.put(reverse('todo-detail',
                                           kwargs={'pk': todo.id}),
                                   data={
                                       "content": "NEW_CONTENT",
                                       "is_done": True
                                   },
                                   format='json')
        new_todo = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(todo.content, new_todo['content'])
        self.assertNotEqual(todo.is_done, new_todo['is_done'])

    def test__delete_todo_when__valid_request__expect__204_no_content(self):
        todo = Todo.objects.get()
        response = self.client.delete(
            reverse('todo-detail', kwargs={'pk': todo.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def _generate_valid_random_todo(self):
        return {"content": fake.paragraph(nb_sentences=5), "is_done": False}
