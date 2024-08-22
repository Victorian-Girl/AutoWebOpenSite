import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def start_automation(links, max_interval, min_duration, max_duration, log_directory, stop_event):                       # fonction start_automation qui prend en paramètres les liens, l'intervalle maximum, la durée minimale et maximale, le dossier de journalisation et l'événement d'arrêt
    # Configurer les options du navigateur Chrome
    options = webdriver.ChromeOptions()                                                                                 # Créer une instance de ChromeOptions
    options.add_argument("--disable-gpu")                                                                               # Ajouter des arguments pour désactiver le GPU, le sandbox et l'utilisation de la mémoire partagée
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")                                                                     # Définir la taille de la fenêtre du navigateur
    options.add_argument("--disable-dev-shm-usage")                                                                     # Ajouter un argument pour désactiver l'utilisation de la mémoire partagée
    options.add_argument("--start-maximized")                                                                           # Ajouter un argument pour démarrer le navigateur en mode maximisé
    options.add_argument("--window-position=-10000,0")                                                                  # Ajouter un argument pour déplacer la fenêtre hors de l'écran
    options.add_argument("--remote-debugging-port=9222")                                                                # Ajouter un argument pour spécifier le port de débogage
    # options.add_argument("--headless")                                                                                  # Décommentez cette ligne pour exécuter en mode headless

    # Créer le dossier des journaux s'il n'existe pas
    os.makedirs(log_directory, exist_ok=True)                                                                           # Créer le dossier de journalisation s'il n'existe pas

    if stop_event.is_set():                                                                                             # Vérifier si l'événement d'arrêt est défini
        return                                                                                                          # Retourner si l'événement d'arrêt est défini

    liens_ouverts = []                                                                                                  # Créer une liste pour stocker les liens déjà ouverts

    while not stop_event.is_set():                                                                                      # Boucle tant que l'événement d'arrêt n'est pas défini
        interval_ouverture = random.randint(1, max_interval)                                                         # Générer un intervalle d'ouverture aléatoire (entre 1 et l'intervalle maximum)
        print(f"Intervalle d'ouverture : {interval_ouverture} minutes")

        duree_ouverture = random.randint(min_duration, max_duration)                                                    # Générer une durée d'ouverture aléatoire (entre la durée minimale et maximale)
        print(f"Durée d'ouverture : {duree_ouverture} minutes")                                                         # Afficher la durée d'ouverture

        service = Service(ChromeDriverManager().install())                                                              # Initialiser le service du pilote Chrome
        driver = webdriver.Chrome(service=service, options=options)                                                     # Initialiser le pilote Chrome avec les options spécifiées

        current_date = datetime.now().strftime("%Y-%m-%d")                                                              # Obtenir la date actuelle
        log_file = os.path.join(log_directory, f"log_{current_date}.txt")                                               # Construire le chemin du fichier journal

        with open(log_file, "a") as f:                                                                                  # Écrire les informations dans le fichier journal
            f.write(f"Intervalle d'ouverture : {interval_ouverture} minutes\n")                                         # Écrire l'intervalle d'ouverture
            f.write(f"Durée d'ouverture : {duree_ouverture} minutes\n")                                                 # Écrire la durée d'ouverture
            f.write(f"Page ouverte à {time.strftime('%H:%M:%S')}\n")                                                    # Écrire l'heure d'ouverture

        try:                                                                                                            # Essayer d'ouvrir la page web

            lien = random.choice([link for link in links if link not in liens_ouverts])                                 # Trouver un lien qui n'a pas été ouvert récemment
            liens_ouverts.append(lien)                                                                                  # Ajouter le lien à la liste des liens ouverts
            if len(liens_ouverts) > len(links):                                                                         # Vérifier si la liste des liens ouverts est plus longue que la liste des liens
                liens_ouverts.pop(0)                                                                                    # Supprimer le lien le plus ancien
            driver.get(lien)                                                                                            # Ouvrir le lien dans le navigateur
            print(f"Page ouverte à {time.strftime('%H:%M:%S')}")                                                        # Afficher l'heure d'ouverture

            with open(log_file, "a") as f:                                                                              # Écrire le lien de la page ouverte dans le fichier journal
                f.write(f"Page ouverte : {lien}\n")                                                                     # Écrire le lien de la page ouverte
                print(f"Page ouverte : {lien}")                                                                         # Afficher le lien de la page ouverte

            for _ in range(duree_ouverture * 60):                                                                       # Boucle pendant la durée d'ouverture (en secondes)
                if stop_event.is_set():                                                                                 # Vérifier si l'événement d'arrêt est défini
                    break                                                                                               # Sortir de la boucle si l'événement d'arrêt est défini
                time.sleep(1)                                                                                           # Attendre 1 seconde

        except Exception as e:                                                                                          # Gérer les exceptions
            print(f"Erreur lors de l'ouverture de la page: {e}")                                                        # Afficher l'erreur

        finally:                                                                                                        # Exécuter le code final
            with open(log_file, "a") as f:                                                                              # Écrire la fermeture de la page dans le fichier journal
                f.write(f"Page fermée à {time.strftime('%H:%M:%S')}\n\n")                                               # Écrire l'heure de fermeture
            driver.quit()                                                                                               # Fermer le navigateur
            print(f"Page fermée à {time.strftime('%H:%M:%S')}")                                                         # Afficher l'heure de fermeture

        for _ in range(interval_ouverture * 60):                                                                        # Attendre jusqu'à la prochaine ouverture (en secondes)
            if stop_event.is_set():                                                                                     # Vérifier si l'événement d'arrêt est défini
                break                                                                                                   # Sortir de la boucle si l'événement d'arrêt est défini
            time.sleep(1)                                                                                               # Attendre 1 seconde


"""
- The code below is the same as the one in main.py made in fist place to test the automation process.



import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Définissez les paramètres de l'automatisation
urls = [
    "https://melissa-c.streamlit.app/",
    "https://melissa-c.streamlit.app/Certificate",
    "https://melissa-c.streamlit.app/Artist_Portfolio",
    "https://melissa-c.streamlit.app/Professional_Portfolio",
    "https://melissens.pythonanywhere.com/",
    "https://melissa.christiaenssens.svija.site/",
    "https://mcrist.artiste.svija.site/",
    "https://victorian-girl.github.io/recette_premiere/"
]

max_interval_ouverture = 2                                                                                              
min_duree_ouverture = 1                                                                                                 
max_duree_ouverture = 1                                                                                                 

# Configurer les options du navigateur Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
options.add_argument("--window-position=-10000,0")
# options.add_argument("--headless")                                                                                    

# Créer le dossier des journaux s'il n'existe pas
log_directory = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_directory, exist_ok=True)

while True:
    # Générer un intervalle d'ouverture aléatoire (entre 1 et 24 heures)
    interval_ouverture = random.randint(1, max_interval_ouverture)
    print(f"Intervalle d'ouverture : {interval_ouverture} minutes")

    # Générer une durée d'ouverture aléatoire (entre 3 et 10 minutes)
    duree_ouverture = random.randint(min_duree_ouverture, max_duree_ouverture)
    print(f"Durée d'ouverture : {duree_ouverture} minutes")

    # Initialiser le navigateur Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Obtenir la date actuelle
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Construire le chemin du fichier journal
    log_file = os.path.join(log_directory, f"log_{current_date}.txt")

    # Écrire les informations dans le fichier journal
    with open(log_file, "a") as f:
        f.write(f"Intervalle d'ouverture : {interval_ouverture} minutes\n")
        f.write(f"Durée d'ouverture : {duree_ouverture} minutes\n")

    try:
        # Ouvrir la page web
        lien = random.choice(urls)
        driver.get(lien)
        print(f"Page ouverte à {time.strftime('%H:%M:%S')}")

        # Écrire le lien de la page ouverte dans le fichier journal
        with open(log_file, "a") as f:
            f.write(f"Page ouverte : {lien}\n")
            f.write(f"Page ouverte à {time.strftime('%H:%M:%S')}\n")

        # Attendre pendant la durée d'ouverture
        time.sleep(duree_ouverture * 60)

    except Exception as e:
        print(f"Erreur lors de l'ouverture de la page: {e}")

    finally:
        # Écrire la fermeture de la page dans le fichier journal
        with open(log_file, "a") as f:
            f.write(f"Page fermée à {time.strftime('%H:%M:%S')}\n\n")
        # Fermer la page web
        driver.quit()
        print(f"Page fermée à {time.strftime('%H:%M:%S')}")

    # Attendre jusqu'à la prochaine ouverture
    time.sleep(interval_ouverture * 60)
"""