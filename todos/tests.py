from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todos.models import Todo


class TodosAPITestCase(APITestCase):
    def create_todo(self):
        sample_todo={'title':'Hello', 'body': 'Test body'}
        return self.client.post(reverse('todos'), sample_todo)

    def authenticate(self):
        #Register test user...
        self.client.post(
            reverse("register"),
            {
                'username': 'gerard',
                'email': 'gerard@gmail.com',
                'password': 'pass=123'
            }
        )
        #Login test user...
        response = self.client.post(
            reverse('login'),
            {
                'email': 'gerard@gmail.com',
                'password': 'pass=123'
            }
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


class TestListCreateTodo(TodosAPITestCase):

    def test_should_not_create_todo_with_no_auth(self):
        response=self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo_with_auth(self):
        #Test createdby auth user
        self.authenticate()
        sample_todo={'title':'Hello', 'body': 'Test body'}
        response=self.client.post(reverse('todos'), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #Test ensure data was sent to db successfully
        self.assertEqual(response.data['title'], 'Hello')
        self.assertEqual(response.data['body'], 'Test body')

        #Check if todo in db
        # previous_todo_count = Todo.objects.all().count()
        # self.assertEqual(Todo.objects.all().count(), previous_todo_count+1)

    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        #post todo for pagination check...
        self.create_todo()

        #get todo to check pagination link is working
        response=self.client.get(reverse('todos'))
        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)


class TestTodoDetailAPIView(TodosAPITestCase):

    def test_retieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        res=self.client.get(reverse('todo', kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #Check that request sent to db is what we get back...
        todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(todo.title, res.data['title'])

    def test_update_one_item(self):
        self.authenticate()
        res = self.create_todo()
        #Add update...
        response = self.client.patch(
            reverse('todo', kwargs={'id': res.data['id']}),
            {"title": "New one", "is_completed": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #Check if Update was added...
        check_updated_todo = Todo.objects.get(id=res.data['id'])
        self.assertEqual(check_updated_todo.is_completed, True)
        self.assertEqual(check_updated_todo.title, 'New one')


    def test_deletes_one_item(self):
        self.authenticate()
        res=self.create_todo()
        prev_db_count=Todo.objects.all().count()
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(
            reverse('todo', kwargs={'id': res.data['id']}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #Make sure our db has no item...
        self.assertEqual(prev_db_count, 0)
