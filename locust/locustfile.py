from locust import HttpUser, task, between

class MovieAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_movies(self):
        self.client.get("/v1/movie", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    @task(2)
    def get_movies_with_params(self):
        self.client.get("/v1/movie?title=star&limit=10", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

