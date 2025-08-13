import os
from datetime import datetime, timedelta

def parse_log(file_path):
    """ Lit le fichier de log et détecte les tentatives de connexion échouées """
    print(f"Tentative d'ouverture du fichier : {file_path}")
    if not os.path.exists(file_path):
        print("Le fichier n'existe pas.")
        return []

    failed_attempts = []
    with open(file_path, 'r') as log_file:
        for line in log_file:
            print(f"Lecture de la ligne : {line.strip()}")
            if "Failed login attempt" in line:
                failed_attempts.append(line.strip())
    
    print(f"Nombre d'échecs trouvés : {len(failed_attempts)}")
    return failed_attempts

def check_alert(failed_attempts, threshold=5, time_window_minutes=10):
    """ Vérifie si le nombre d'échecs dépasse le seuil dans un intervalle de temps donné. """
    
    # Convertir les dates en format datetime pour la comparaison
    failed_times = []
    for attempt in failed_attempts:
        date_str = attempt.split(' ')[0] + ' ' + attempt.split(' ')[1]  # Date et heure (ex : 2025-08-08 14:25:01)
        timestamp = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        failed_times.append(timestamp)

    # Vérifier les échecs dans un intervalle de temps
    alerts = []
    for i in range(len(failed_times)):
        current_time = failed_times[i]
        window_start = current_time - timedelta(minutes=time_window_minutes)
        
        # Compter le nombre d'échecs dans l'intervalle de temps
        count = sum(1 for t in failed_times if window_start <= t <= current_time)
        
        if count >= threshold:
            alerts.append(f"ALERTE : {count} tentatives échouées détectées entre {window_start} et {current_time}")
    
    return alerts

def main():
    """ Fonction principale qui gère le processus de détection et d'alerte """
    LOG_FILE_PATH = r"C:\Users\oumar\Desktop\test_log.txt"  # Change ici le chemin si nécessaire
    print(f"Chemin du fichier : {LOG_FILE_PATH}")
    
    failed_attempts = parse_log(LOG_FILE_PATH)
    
    if failed_attempts:
        print(f"Échecs détectés : {failed_attempts}")
        alerts = check_alert(failed_attempts)
        
        if alerts:
            print("Alertes :")
            for alert in alerts:
                print(alert)
        else:
            print("Pas d'alerte. Pas assez d'échecs dans la période spécifiée.")
    else:
        print("Aucun échec détecté.")

# Exécution de la fonction principale
if __name__ == "__main__":
    main()