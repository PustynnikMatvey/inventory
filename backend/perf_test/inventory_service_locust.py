import random

from locust import HttpUser, task, between

MIN_USER_ID = 1
MAX_USER_ID = 10**6


class InventoryUser(HttpUser):
    wait_time = between(1, 2)  # Wait between 1 and 2 seconds between tasks
    inventory_items = ('test_item', 'bfg', 'bla')

    @task
    def get_inventory(self):
        player_id = random.randint(MIN_USER_ID, MAX_USER_ID)
        self.client.post("api/v1/get_inventory", json={"player_id": player_id})