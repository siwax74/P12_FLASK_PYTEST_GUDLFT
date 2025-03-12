from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les tâches

    @task
    def index(self):
        """Accéder à la page d'accueil"""
        self.client.get("/")

    @task
    def show_summary(self):
        """Simuler une connexion et affichage du récapitulatif"""
        self.client.post("/showSummary", data={"email": "john@club.com"})

    @task
    def book_competition(self):
        """Réserver une compétition"""
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def purchase_places(self):
        """Acheter des places pour une compétition"""
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "2"
        })

    @task
    def show_table_point(self):
        """Afficher le tableau des points"""
        self.client.get("/showTablePoint")

    @task
    def logout(self):
        """Se déconnecter"""
        self.client.get("/logout")
