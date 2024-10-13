import json

from locust import HttpUser, TaskSet, task, User


class CartBehavior(TaskSet):

    def __init__(self, parent: User):
        super().__init__(parent)
        self.cart_id = None

    def on_start(self):
        response = self.client.post("/cart")
        self.cart_id = json.loads(response.text)['id']

    @task(1)
    def get_cart(self):
        self.client.get(f'/cart/{self.cart_id}')

class WebsiteUser(HttpUser):
    tasks = [CartBehavior]
    min_wait = 5000
    max_wait = 9000
