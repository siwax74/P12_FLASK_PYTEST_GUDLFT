# Gudlift-Registration (Branch QA)

## Why

Cette branche **QA** est dédiée aux tests de performance et à la couverture de code. Elle utilise les outils suivants pour garantir la qualité et les performances de l'application :

- **pytest** : Pour les tests unitaires et fonctionnels.
- **locust** : Pour les tests de charge et de performance.
- **pytest-cov** : Pour mesurer la couverture de code des tests.

## Getting Started

Cette branche utilise les mêmes technologies de base que la branche **master** :

- **Python v3.x+**
- **Flask**
- **Virtual environment**

### Installation

1. **Cloner le dépôt et changer de branche :**
   ```bash
   git clone git@github.com:siwax74/P12_FLASK_PYTEST_GUDLFT.git
   cd P12_FLASK_PYTEST_GUDLFT
   git checkout QA
   ```

2. **Créer et activer un environnement virtuel :**
   ```bash
   source env/bin/activate # Sur Mac/Linux
   env\Scripts\activate    # Sur Windows
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

### Lancement de l'application

Pour exécuter l'application, utilisez l'une des commandes suivantes :
```bash
$env:FLASK_APP="src/server.py"
$env:FLASK_ENV="development"
flask run
```

L'application sera accessible via l'adresse indiquée dans le terminal (par défaut : http://127.0.0.1:5000).

---

## Testing

### Tests Unitaires et Fonctionnels avec Pytest

Pour exécuter les tests unitaires et fonctionnels avec **pytest**, utilisez la commande suivante :
```bash
cd tests
pytest -v # Affiche tous les testset leur statut
pytest -s # Voir les message de tests(print)
```

Pour générer un rapport de couverture de code avec **pytest-cov**, exécutez :
```bash
pytest --cov=./
```

Les rapports de couverture seront affichés directement dans la console.

#### Générer un rapport HTML de la couverture
Pour obtenir un rapport HTML plus lisible :
```bash
pytest --cov=./ --cov-report=html
```

Le rapport HTML sera généré dans le dossier `htmlcov/`, que vous pouvez ouvrir dans votre navigateur.
```bash
http://127.0.0.1:5500/htmlcov/index.html
```

---
### Tests de Performance avec Locust

Pour tester les performances de l'application avec **Locust** :
1. Assurez-vous que l'application est en cours d'exécution.
2. Assurez vous d'être dans le dossier tests.
3. Exécutez Locust avec la commande suivante :
   ```bash
   locust -f locustfile.py
   ```
4. Rendez-vous ensuite sur l'interface web de Locust (par défaut : [http://127.0.0.1:8089](http://127.0.0.1:8089)).
5. Configurez le nombre d'utilisateurs et le taux de lancement, puis démarrez les tests.

---

## Bonnes Pratiques

- Mettez à jour les dépendances dans le fichier `requirements.txt` après l'ajout d'un nouvel outil :
  ```bash
  pip freeze > requirements.txt
  ```
- Vérifiez régulièrement la couverture des tests pour vous assurer d'un bon niveau de qualité.
- Exécutez les tests de performance après des changements majeurs pour garantir la stabilité.

---

## Contributions

Les contributions sont les bienvenues ! Merci de créer une nouvelle branche pour vos fonctionnalités ou correctifs et de soumettre une *pull request* après les tests.

---

Si vous avez des questions ou des suggestions, n'hésitez pas à me contacter. 🎉