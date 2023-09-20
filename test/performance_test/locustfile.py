from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def showsummary(self, validate_club):
        self.client.post('/showSummary', {'email': validate_club['email']})

    @task(6)
    def login(self):
        self.client.get('/')

    @task
    def logout(self):
        self.client.get('/logout')
