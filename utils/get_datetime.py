from datetime import datetime, timezone

def get_current_datetime():
    #Gibt das aktuelle Datum und die Uhrzeit im Format 'YYYY-MM-DD HH:MM:SS' zurück.
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_current_datetime_aware_utc():
    # Gibt das aktuelle Datum und die Uhrzeit als timezone-aware UTC datetime Objekt zurück.
    return datetime.now(timezone.utc)

def get_date():
    #Gibt das aktuelle Datum im Format 'DD.MM.YYYY' zurück.
    return datetime.now().strftime('%d.%m.%Y')

def get_time():
    #Gibt die aktuelle Uhrzeit im Format 'HH:MM' zurück.
    return datetime.now().strftime('%H:%M')