from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    """
    performance test
    """
    @task
    def showsummary(self):
        """
        simulate a POST request to the showSummary with validate email.
        """
        self.client.post('/showSummary', {'email': 'admin@irontemple.com'})

    @task(6)
    def login(self):
        self.client.get('/')

    @task
    def logout(self):
        self.client.get('/logout')
