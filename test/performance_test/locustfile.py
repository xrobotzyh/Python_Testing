from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def showsummary(self):
        self.client.post('/showSummary', {'email': 'admin@irontemple.com'})

    @task(6)
    def login(self):
        self.client.get('/')

    @task
    def logout(self):
        self.client.get('/logout')
