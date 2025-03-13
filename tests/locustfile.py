from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente entre les tâches

    def on_start(self):
        """Initialisation des données avant chaque tâche"""
        # Initialiser les variables à l'intérieur de on_start
        self.email = "john@simplylift.co"
        self.competition = "Spring Festival"
        self.club = "Simply Lift"

    @task
    def index(self):
        """Accéder à la page d'accueil"""
        self.client.get("/")

    @task
    def show_summary(self):
        """Simuler une connexion et affichage du récapitulatif"""
        self.client.post("/showSummary", data={"email": self.email})

    @task
    def book_competition(self):
        """Réserver une compétition"""
        # Utilisation des variables définies dans on_start
        self.client.get(f"/book/{self.competition}/{self.club}")

    @task
    def purchase_places(self):
        """Acheter des places pour une compétition"""
        self.client.post("/purchasePlaces", data={
            "competition": self.competition,
            "club": self.club,
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
