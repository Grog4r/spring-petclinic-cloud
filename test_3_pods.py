import requests
import concurrent.futures
import time
from collections import Counter

# --- Konfiguration ---
# Die URL Ihres Spring Boot Microservice Endpunkts
# Ersetzen Sie 'YOUR_EXTERNAL_IP' durch die tatsächliche externe IP Ihres Kubernetes Service
# und stellen Sie sicher, dass der Pfad korrekt ist (z.B. /appointments/info)
TARGET_URL = "http://10.105.114.155/api/appointments/appointments/info"

# Anzahl der parallelen Anfragen, die gesendet werden sollen
NUM_PARALLEL_REQUESTS = 20

# Anzahl der Wiederholungen für jede parallele Anfrage (um das Load Balancing besser zu sehen)
NUM_REPEATS_PER_THREAD = 5

# --- Funktion zum Senden einer einzelnen Anfrage ---
def send_request(url, request_num, thread_id):
    """
    Sendet eine GET-Anfrage an die gegebene URL und gibt die Antwort aus.
    Gibt den Hostnamen (Pod-Namen) zurück, von dem die Antwort kam.
    """
    try:
        # Verwenden Sie 'Connection: close' Header, um sicherzustellen, dass die Verbindung
        # nach jeder Anfrage geschlossen wird. Dies hilft, das Load Balancing zu erzwingen,
        # indem verhindert wird, dass die Verbindung wiederverwendet wird (ähnlich wie curl --fresh-connect).
        headers = {'Connection': 'close'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Löst eine HTTPError für schlechte Antworten (4xx oder 5xx) aus

        response_text = response.text.strip()
        # Extrahieren des Hostnamens aus der Antwort, z.B. "Handled by Pod: petclinic-appointments-deployment-abcde"
        # Annahme: Die Antwort enthält "Handled by Pod: <HOSTNAME>"
        host_info = "Unbekannt"
        if "Handled by Pod:" in response_text:
            host_info = response_text.split("Handled by Pod:")[1].strip()

        print(f"Thread {thread_id}, Anfrage {request_num}: Status Code {response.status_code}, Host: {host_info}")
        return host_info # Gibt den Hostnamen zurück
    except requests.exceptions.RequestException as e:
        print(f"Thread {thread_id}, Anfrage {request_num}: Fehler beim Senden der Anfrage: {e}")
        return None # Gibt None zurück bei Fehlern

# --- Hauptteil des Skripts ---
if __name__ == "__main__":
    print(f"Sende {NUM_PARALLEL_REQUESTS} parallele Anfragen (jeweils {NUM_REPEATS_PER_THREAD} Wiederholungen) an: {TARGET_URL}\n")

    start_time = time.time()
    
    # Liste zum Speichern der Host-Antworten
    all_responses = []

    # Erstellen Sie einen Thread-Pool-Executor
    # max_workers bestimmt die maximale Anzahl von Threads, die gleichzeitig ausgeführt werden können
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_PARALLEL_REQUESTS) as executor:
        # Speichern Sie die Future-Objekte, um auf den Abschluss der Aufgaben zu warten
        futures = []
        for i in range(NUM_PARALLEL_REQUESTS):
            for j in range(NUM_REPEATS_PER_THREAD):
                # Senden Sie die Aufgabe an den Executor
                futures.append(executor.submit(send_request, TARGET_URL, j + 1, i + 1))

        # Warten Sie auf den Abschluss aller Aufgaben und verarbeiten Sie Ergebnisse/Ausnahmen
        for future in concurrent.futures.as_completed(futures):
            host = future.result() # Holen Sie das Ergebnis der send_request Funktion
            if host:
                all_responses.append(host)

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nAlle Anfragen abgeschlossen in {duration:.2f} Sekunden.")

    # Zählen und Anzeigen der Antworten pro Host
    if all_responses:
        host_counts = Counter(all_responses)
        print("\n--- Zusammenfassung der Antworten pro Host ---")
        for host, count in host_counts.items():
            print(f"Host '{host}': {count} Antworten")
    else:
        print("\nKeine Antworten erhalten oder Host-Informationen konnten nicht extrahiert werden.")

