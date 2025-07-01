"""
Plik konfiguracyjny projektu

Zawiera:
- Klucz API do The Movie Database
- URL bazowy API
- Inne stałe i ustawienia programu
"""

from dotenv import load_dotenv
import os

load_dotenv()

# Twój klucz API z TMDb (zastąp 'twój_klucz_api' swoim prawdziwym kluczem)
API_KEY = os.getenv("API_KEY")
# Bazowy URL API
BASE_URL = os.getenv("BASE_URL")
# Język odpowiedzi (możesz ustawić 'pl' dla polskiego)
LANGUAGE = os.getenv("LANGUAGE")
# Ścieżka do zapisywania danych użytkownika
USER_DATA_FILE = "user_data.json"