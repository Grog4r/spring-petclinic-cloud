import requests
import concurrent.futures
import time
from collections import Counter
import os


svc = os.popen('kubectl get svc api-gateway -n spring-petclinic').read()

IP = svc.split("\n")[1].split()[3]
print(IP)


TARGET_URL = f"http://{IP}/api/appointments/appointments/info"

# Anzahl der parallelen Anfragen, die gesendet werden sollen
NUM_PARALLEL_REQUESTS = 20

# Anzahl der Wiederholungen für jede parallele Anfrage (um das Load Balancing besser zu sehen)
NUM_REPEATS_PER_THREAD = 5

def send_request(url, request_num, thread_id):
    """
    Sendet eine GET-Anfrage an die gegebene URL und gibt die Antwort aus.
    Gibt den Hostnamen (Pod-Namen) zurück, von dem die Antwort kam.
    """
    try:
        headers = {'Connection': 'close'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Löst eine HTTPError für schlechte Antworten (4xx oder 5xx) aus

        response_text = response.text.strip()
        
        host_info = "Unbekannt"
        if "Handled by Pod:" in response_text:
            host_info = response_text.split("Handled by Pod:")[1].strip()

        print(f"Thread {thread_id}, Anfrage {request_num}: Status Code {response.status_code}, Host: {host_info}")
        return host_info
    except requests.exceptions.RequestException as e:
        print(f"Thread {thread_id}, Anfrage {request_num}: Fehler beim Senden der Anfrage: {e}")
        return None

if __name__ == "__main__":
    print(f"Sende {NUM_PARALLEL_REQUESTS} parallele Anfragen (jeweils {NUM_REPEATS_PER_THREAD} Wiederholungen) an: {TARGET_URL}\n")

    start_time = time.time()
    
    all_responses = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_PARALLEL_REQUESTS) as executor:
        futures = []
        for i in range(NUM_PARALLEL_REQUESTS):
            for j in range(NUM_REPEATS_PER_THREAD):
                futures.append(executor.submit(send_request, TARGET_URL, j + 1, i + 1))

        for future in concurrent.futures.as_completed(futures):
            host = future.result()
            if host:
                all_responses.append(host)

    end_time = time.time()
    duration = end_time - start_time

    print(f"\nAlle Anfragen abgeschlossen in {duration:.2f} Sekunden.")

    if all_responses:
        host_counts = Counter(all_responses)
        print("\n--- Zusammenfassung der Antworten pro Host ---")
        for host, count in host_counts.items():
            print(f"Host '{host}': {count} Antworten")
    else:
        print("\nKeine Antworten erhalten oder Host-Informationen konnten nicht extrahiert werden.")

