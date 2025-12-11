"""Track IP

Diesen Modul wird benutzt, um IP-Adressen zu überwachen und den Zugriff basierend auf einer Whitelist zu steuern.

"""

# Importiert notwendige Bibliotheken
from functools import wraps
from flask import request, abort

# Definiert eine Liste erlaubter IP-Adressen
allowed_ips = [
    "127.0.0.1",
]

# Dekorator-Funktion zur Überprüfung der IP-Adresse
def whitlist_ips(allowed_ips):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("IP Adresse wird überprüft...")
            client_ip = request.remote_addr
            if client_ip not in allowed_ips:
                print(f"Zugriff verweigert für IP: {client_ip}")
                abort(403)  # Forbidden
            print(f"Zugriff erlaubt für IP: {client_ip}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator