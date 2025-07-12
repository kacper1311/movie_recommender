"""
Plik konfiguracyjny projektu

Zawiera:
- Klucz API do The Movie Database (pobierany z pliku .env)
- URL bazowy API
- Inne stałe i ustawienia programu
- Konfigurację bezpieczeństwa (klucze API w zmiennych środowiskowych)

UWAGA: Plik .env z kluczem API NIE powinien być commitowany do repozytorium!
"""

from dotenv import load_dotenv
import os

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Twój klucz API z TMDb (pobierany z pliku .env dla bezpieczeństwa)
API_KEY = os.getenv("API_KEY")
# Bazowy URL API TMDb
BASE_URL = os.getenv("BASE_URL", "https://api.themoviedb.org/3")
# Język odpowiedzi (możesz ustawić 'pl' dla polskiego)
LANGUAGE = os.getenv("LANGUAGE", "pl")
# Ścieżka do zapisywania danych użytkownika
USER_DATA_FILE = "user_data.json"

# Sprawdzenie czy klucz API jest dostępny
if not API_KEY:
    print("UWAGA: Klucz API nie został znaleziony w pliku .env!")
    print("Utwórz plik .env z zawartością:")
    print("API_KEY=twój_klucz_api")
    print("BASE_URL=https://api.themoviedb.org/3")
    print("LANGUAGE=pl")