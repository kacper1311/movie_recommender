# System Rekomendacji Filmów - Projekt Python

## O Projekcie

### Co to jest?
Stworzyłem system rekomendacji filmów, który pomaga użytkownikom znaleźć filmy, które mogą im się spodobać na podstawie ich wcześniejszych ocen. Program wykorzystuje API The Movie Database (TMDb) do pobierania informacji o filmach i implementuje algorytm rekomendacji oparty na preferencjach użytkownika.

### Dlaczego to zrobiłem?
Projekt powstał jako zadanie z programowania w Pythonie, gdzie miałem zaimplementować różne koncepcje programistyczne takie jak:
- Klasy i obiekty
- Listy składane i generatory
- Obsługa błędów i wyjątków
- Praca z API zewnętrznym
- Analiza danych z NumPy
- Zapisywanie i wczytywanie danych JSON

## Jak to działa?

### Główne funkcjonalności:

#### 1. **Wyszukiwanie filmów** 🔍
- Możesz wyszukać dowolny film po nazwie
- Program łączy się z TMDb API i pokazuje wyniki wyszukiwania
- Dla każdego filmu wyświetla: tytuł, rok, gatunek, średnią ocenę, czas trwania

#### 2. **Historia oglądania** 📺
- Dodajesz filmy do swojej historii oglądania podając ich ID
- Program zapisuje wszystkie obejrzane filmy w pliku JSON
- Możesz przeglądać swoją historię oglądania

#### 3. **System oceniania** ⭐
- Oceniasz filmy z historii oglądania w skali 1-10
- Program pokazuje tylko nieocenione filmy z historii
- Możesz zmieniać oceny już ocenionych filmów
- Wszystkie oceny są zapisywane automatycznie

#### 4. **Algorytm rekomendacji** 🧠
Program analizuje Twoje oceny i:
- Oblicza Twoje ulubione gatunki na podstawie ocen
- Generuje rekomendacje filmów z tych gatunków
- Uwzględnia zarówno Twoje preferencje (70%) jak i oceny TMDb (30%)
- Wyklucza filmy, które już oceniłeś

#### 5. **Filmy do ponownego obejrzenia** 🔄
- Pokazuje filmy z Twoimi wysokimi ocenami (≥7/10)
- Sortuje je według Twoich ocen (od najwyższej)
- Idealne do przypomnienia sobie ulubionych filmów

#### 6. **Statystyki użytkownika** 📊
- Liczba ocenionych filmów
- Średnia ocena i odchylenie standardowe
- Ulubiony gatunek i top 3 gatunki
- Liczba obejrzanych filmów

#### 7. **Wyszukiwanie podobnych filmów** 🔗
- Podajesz ID filmu, który Ci się podobał
- Program znajduje filmy z podobnymi gatunkami
- Sortuje według podobieństwa gatunków i oceny TMDb

## Jak uruchomić projekt?

### Krok 1: Przygotowanie środowiska
```bash
# Utwórz środowisko wirtualne
python -m venv venv

# Aktywuj środowisko
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

### Krok 2: Konfiguracja API
1. Utwórz plik `.env` w głównym katalogu
2. Dodaj swój klucz API z TMDb:
```
API_KEY=twój_klucz_api_z_tmdb
BASE_URL=https://api.themoviedb.org/3
LANGUAGE=pl
```

**Jak zdobyć klucz API?**
1. Wejdź na https://www.themoviedb.org/
2. Zarejestruj się i zaloguj
3. Przejdź do Settings → API
4. Złóż wniosek o klucz API
5. Skopiuj klucz do pliku .env

### Krok 3: Uruchomienie
```bash
python main.py
```

## Struktura projektu

### Pliki główne:
- **`main.py`** - Główny plik programu z interfejsem użytkownika
- **`recommender.py`** - Algorytm rekomendacji filmów
- **`models.py`** - Klasy Movie i User
- **`api.py`** - Komunikacja z TMDb API
- **`config.py`** - Konfiguracja i zmienne środowiskowe

### Pliki pomocnicze:
- **`test_api.py`** - Testy jednostkowe
- **`requirements.txt`** - Zależności projektu
- **`.env`** - Klucz API (nie commitowany)
- **`user_data.json`** - Dane użytkownika

## Szczegóły implementacji

### Klasy i obiekty:
- **Klasa `Movie`** - reprezentuje film z atrybutami: movie_id, title, year, avg_rating, runtime, genres
- **Klasa `User`** - reprezentuje użytkownika z: user_id, user_name, user_ratings, user_watch_history
- **Klasa `MovieRecommender`** - algorytm rekomendacji z: user, genre_weights, favorite_genres

### Listy składane i generatory:
- Używam list składanych do filtrowania filmów i obliczania statystyk
- Generatory do efektywnego przetwarzania danych użytkownika
- Przykłady w `recommender.py` i `models.py`

### Obsługa błędów:
- Try/except dla komunikacji z API
- Walidacja danych wejściowych
- Obsługa błędów plików JSON
- Komunikaty błędów dla użytkownika

### Praca z API:
- **`search_movies(query)`** - Wyszukuje filmy po nazwie
- **`movie_for_id(id)`** - Pobiera szczegóły filmu po ID
- **`runtime(id)`** - Pobiera czas trwania filmu

### Analiza danych z NumPy:
- Obliczanie średniej oceny i odchylenia standardowego
- Analiza preferencji użytkownika
- Statystyki gatunków filmowych

## Algorytm rekomendacji - jak to działa?

### 1. Analiza preferencji użytkownika:
- Program analizuje wszystkie Twoje oceny
- Dla każdego gatunku oblicza średnią ocenę
- Sortuje gatunki według preferencji

### 2. Generowanie rekomendacji:
- Wybiera top 3 ulubione gatunki
- Wyszukuje filmy z tych gatunków w TMDb
- Wyklucza filmy już ocenione przez Ciebie
- Oblicza wynik rekomendacji: 70% preferencje + 30% ocena TMDb

### 3. Sortowanie wyników:
- Sortuje filmy według wyniku rekomendacji
- Zwraca top N rekomendacji

## Bezpieczeństwo

### Ochrona klucza API:
- Klucz API jest przechowywany w pliku `.env`
- Plik `.env` jest dodany do `.gitignore`
- Program sprawdza czy klucz jest dostępny przy uruchomieniu

### Walidacja danych:
- Sprawdzanie poprawności ocen (1-10)
- Walidacja ID filmów
- Obsługa błędów API i plików

## Testowanie

### Uruchomienie testów:
```bash
python test_api.py
```

### Co testuję:
- Komunikację z API TMDb
- Tworzenie obiektów Movie
- Funkcjonalność użytkownika
- Algorytm rekomendacji

## Możliwe rozszerzenia

### Co mógłbym dodać w przyszłości:
1. **Interfejs webowy** - Flask/Django
2. **Baza danych** - SQLite/PostgreSQL
3. **Więcej algorytmów** - Collaborative Filtering
4. **Analiza sentymentu** - recenzje użytkowników
5. **Grafika** - wykresy preferencji
6. **Eksport danych** - CSV, Excel

---
**Autor:** Kacper Jasyk
