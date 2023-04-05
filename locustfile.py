from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def view_homepage(self):
        self.client.get("/")