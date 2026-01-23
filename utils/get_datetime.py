from datetime import datetime, timezone, date, timedelta

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

def get_datetime_formatted():
    #Gibt das aktuelle Datum im ISO 8601 Format 'YYYY-MM-DD' zurück.
    return date.today().isoformat()

def get_current_time_format():
    #Gibt die aktuelle Uhrzeit im Format 'HH:MM' zurück.
    return datetime.now().strftime("%H:%M")

def get_date_of_weekday(target_weekday_name):
    """
    Gibt das Datum des gewünschten Wochentags der aktuellen Woche zurück.
    Format: 'YYYY-MM-DD'
    Eingabe: Wochentag auf Deutsch (z.B. "Montag")
    """
    weekdays = {
        "Montag": 0, "Dienstag": 1, "Mittwoch": 2, "Donnerstag": 3,
        "Freitag": 4, "Samstag": 5, "Sonntag": 6
    }
    
    target_weekday_name = target_weekday_name.capitalize()
    if target_weekday_name not in weekdays:
        return "Ungültiger Wochentag"

    today = datetime.now()
    # current_weekday: Montag=0, Sonntag=6
    current_weekday = today.weekday()
    target_weekday_index = weekdays[target_weekday_name]
    
    # Differenz berechnen (Ziel - Aktuell)
    delta_days = target_weekday_index - current_weekday
    
    # Das Datum berechnen
    target_date = today + timedelta(days=delta_days)
    
    return target_date.strftime('%Y-%m-%d')