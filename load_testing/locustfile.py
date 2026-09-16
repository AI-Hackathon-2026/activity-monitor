import uuid

from locust import HttpUser, task


class MyUser(HttpUser):
    @task
    def post_whoami(self):
        payload = {
            "request_id": str(uuid.uuid4()),
            "data": {"key": "value"},
            "metadata": {"source": "test"},
        }
        self.client.post("/api/v1/whoami/log", json=payload)
