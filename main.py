"""
Główny plik programu System Rekomendacji Filmów

Odpowiada za:
- Interfejs użytkownika (menu, wyświetlanie wyników)
- Główną pętlę programu
- Integrację wszystkich modułów systemu
- Integrację algorytmu rekomendacji z interfejsem użytkownika
"""
from api import search_movies, movie_for_id
from models import User
from models import Movie
from recommender import create_recommender


class MovieRecomenderApp:
    def __init__(self):
        self.user = User(1, "Kacper")
        self.recommender = create_recommender(self.user)
    
    
    # Funkcje do wyświetalnia menu.
    def display_main_menu(self):
        print("\n--- MENU ---")
        print("1. Wyszukaj film")
        print("2. Zobacz listę obejrzanych filmów")
        print("3. Zarządzaj ocenami")
        print("4. Sprawdź rekomendowane filmy")
        print("5. Filmy do ponownego obejrzenia")
        print("6. Statystyki użytkownika")
        print("7. Znajdź podobne filmy")
        print("8. Zamknij program")
        
        
    def display_movie_menu(self):
        print("\n --- ZARZADZANIE AKCJAMI NA FILMACH ---")
        print("1. Dodaj film do historii ogladania ")
        print("2. Oceń film")
        print("3. Ponownie wyszukaj film")
        print("4. Wróć do menu głównego")
        
        
    def display_ratings_menu(self):
        print("\n --- ZARZĄDZANIE OCENAMI ---")
        print("1. Oceń film z historii")
        print("2. Zobacz swoje oceny")
        print("3. Zmień ocenę filmu")
        print("4. Wróć do menu głównego")
        
        
    def display_recommendations_menu(self):
        print("\n --- REKOMENDACJE FILMÓW ---")
        print("1. Pokaż rekomendowane filmy")
        print("2. Pokaż filmy do ponownego obejrzenia")
        print("3. Statystyki użytkownika")
        print("4. Wróć do menu głównego")
        
        
    # Pobieranie danych od uzytkownika    
    def get_user_input(self, prompt, type_cast=int):
        while True:
            try:
                return type_cast(input(prompt))
            except ValueError:
                print(f"\nNieprawidłowa warość! Wprowadź {type_cast.__name__}.")
                
                
    # Funkcja do obsługi rekomendacji
    def handle_recommendations_menu(self):
        while True:
            self.display_recommendations_menu()
            option = self.get_user_input("\n Wybierz opcję: ", int)
            
            if option == 1:
                self.show_recommended_movies()
                
            elif option == 2:
                self.show_rewatch_recommendations()
                
            elif option == 3:
                self.show_user_statistics()
                
            elif option == 4:
                return  # Wraca do głównego menu
                
            else:
                print("\nNieprawidłowa opcja!")
    
    def show_recommended_movies(self):
        """Wyświetla rekomendowane filmy na podstawie preferencji użytkownika"""
        print("\n--- REKOMENDOWANE FILMY ---")
        
        if not self.user.user_ratings:
            print("Najpierw oceń kilka filmów, żeby otrzymać rekomendacje!")
            return
        
        recommendations = self.recommender.get_recommendations(limit=10)
        
        if not recommendations:
            print("Nie znaleziono rekomendacji. Spróbuj ocenić więcej filmów.")
            return
        
        print(f"Znaleziono {len(recommendations)} rekomendowanych filmów:\n")
        
        for i, (movie, score) in enumerate(recommendations, 1):
            print(f"{i}. {movie.title} ({movie.year})")
            print(f"   Gatunek: {movie.genres}")
            print(f"   Średnia ocena TMDb: {movie.avg_rating}/10")
            print(f"   Wynik rekomendacji: {score:.2f}")
            print(f"   ID filmu: {movie.movie_id}\n")
    
    def show_rewatch_recommendations(self):
        """Wyświetla filmy do ponownego obejrzenia"""
        print("\n--- FILMY DO PONOWNEGO OBJRZENIA ---")
        
        if not self.user.user_ratings:
            print("Najpierw oceń kilka filmów!")
            return
        
        rewatch_recommendations = self.recommender.get_rewatch_recommendations(limit=5)
        
        if not rewatch_recommendations:
            print("Nie masz jeszcze filmów z wysokimi ocenami do ponownego obejrzenia.")
            return
        
        print(f"Znaleziono {len(rewatch_recommendations)} filmów do ponownego obejrzenia:\n")
        
        for i, (movie, user_rating) in enumerate(rewatch_recommendations, 1):
            print(f"{i}. {movie.title} ({movie.year})")
            print(f"   Twoja ocena: {user_rating * 10:.1f}/10")
            print(f"   Gatunek: {movie.genres}")
            print(f"   Średnia ocena TMDb: {movie.avg_rating}/10")
            print(f"   ID filmu: {movie.movie_id}\n")
    
    def show_user_statistics(self):
        """Wyświetla statystyki użytkownika"""
        print("\n--- STATYSTYKI UŻYTKOWNIKA ---")
        
        stats = self.recommender.get_user_statistics()
        
        print(f"Liczba ocenionych filmów: {stats['total_rated']}")
        print(f"Średnia ocena: {stats['average_rating']:.2f}/10")
        if stats['rating_std'] > 0:
            print(f"Odchylenie standardowe ocen: {stats['rating_std']:.2f}")
        print(f"Liczba obejrzanych filmów: {stats['total_watched']}")
        
        if stats['favorite_genre']:
            print(f"Ulubiony gatunek: {stats['favorite_genre']}")
        
        if stats['top_genres']:
            print(f"Top 3 gatunki: {', '.join(stats['top_genres'])}")
    
    def handle_similar_movies(self):
        """Obsługuje wyszukiwanie podobnych filmów"""
        print("\n--- ZNAJDŹ PODOBNE FILMY ---")
        
        movie_id = self.get_user_input("Podaj ID filmu, dla którego chcesz znaleźć podobne: ", int)
        
        similar_movies = self.recommender.get_similar_movies(movie_id, limit=5)
        
        if not similar_movies:
            print("Nie znaleziono podobnych filmów lub film o podanym ID nie istnieje.")
            return
        
        print(f"Znaleziono {len(similar_movies)} podobnych filmów:\n")
        
        for i, movie in enumerate(similar_movies, 1):
            print(f"{i}. {movie.title} ({movie.year})")
            print(f"   Gatunek: {movie.genres}")
            print(f"   Średnia ocena: {movie.avg_rating}/10")
            print(f"   ID filmu: {movie.movie_id}\n")
                
    def show_unrated_movies_from_history(self):
        """Wyświetla tylko nieocenione filmy z historii oglądania"""
        print("\n--- FILMY Z HISTORII DO OCENIENIA ---")
        
        if not self.user.user_watch_history:
            print("Nie masz jeszcze filmów w historii oglądania.")
            return []
        
        # Znajdź tylko nieocenione filmy z historii
        unrated_movies = []
        for movie_id in self.user.user_watch_history:
            if str(movie_id) not in self.user.user_ratings:  # Konwertuj na string dla porównania
                movie = movie_for_id(movie_id)
                if movie:
                    unrated_movies.append(movie)
        
        if not unrated_movies:
            print("Wszystkie filmy z historii zostały już ocenione!")
            return []
        
        print(f"Znaleziono {len(unrated_movies)} nieocenionych filmów:\n")
        
        for i, movie in enumerate(unrated_movies, 1):
            print(f"{i}. {movie.title} ({movie.year})")
            print(f"   Gatunek: {movie.genres}")
            print(f"   Średnia ocena TMDb: {movie.avg_rating}/10")
            print(f"   ID filmu: {movie.movie_id}")
            print(f"   Status: Nie oceniony")
            print()
        
        return unrated_movies
    
    def show_rated_movies(self):
        """Wyświetla ocenione filmy z możliwością zmiany oceny"""
        print("\n--- TWOJE OCENIONE FILMY ---")
        
        if not self.user.user_ratings:
            print("Nie oceniłeś jeszcze żadnego filmu.")
            return []
        
        rated_movies = []
        for movie_id, rating in self.user.user_ratings.items():
            movie = movie_for_id(int(movie_id))
            if movie:
                rated_movies.append((movie, rating))
        
        print(f"Oceniłeś {len(rated_movies)} filmów:\n")
        
        for i, (movie, rating) in enumerate(rated_movies, 1):
            print(f"{i}. {movie.title} ({movie.year})")
            print(f"   Twoja ocena: {rating}/10")
            print(f"   Gatunek: {movie.genres}")
            print(f"   Średnia ocena TMDb: {movie.avg_rating}/10")
            print(f"   ID filmu: {movie.movie_id}")
            print()
        
        return rated_movies
    
    def handle_ratings_menu(self):
        while True:
            self.display_ratings_menu() # Wyświetla menu ocen.
            option = self.get_user_input("\n Wybierz opcję: ", int) # Pobiera zapytanie o wybór opcji od uzytkownika
            
            if option == 1:
                # Pokaż tylko nieocenione filmy z historii
                unrated_movies = self.show_unrated_movies_from_history()
                
                if unrated_movies:
                    print("Wybierz film do ocenienia:")
                    print("0. Wróć do menu ocen")
                    
                    for i, movie in enumerate(unrated_movies, 1):
                        print(f"{i}. {movie.title} (ID: {movie.movie_id})")
                    
                    choice = self.get_user_input("\nWybierz numer filmu (0-{0}): ".format(len(unrated_movies)), int)
                    
                    if choice == 0:
                        continue
                    elif 1 <= choice <= len(unrated_movies):
                        selected_movie = unrated_movies[choice - 1]
                        print(f"\nOceniasz film: {selected_movie.title}")
                        
                        self.user.rate_movie(selected_movie.movie_id)
                        # Aktualizuj rekomender po dodaniu oceny
                        self.recommender = create_recommender(self.user)
                        print("Film został oceniony i usunięty z listy nieocenionych!")
                    else:
                        print("Nieprawidłowy wybór!")
                
            elif option == 2:
                self.user.load_ratings()
                
            elif option == 3:
                # Pokaż ocenione filmy z możliwością zmiany oceny
                rated_movies = self.show_rated_movies()
                
                if rated_movies:
                    print("Wybierz film do zmiany oceny:")
                    print("0. Wróć do menu ocen")
                    
                    for i, (movie, rating) in enumerate(rated_movies, 1):
                        print(f"{i}. {movie.title} (obecna ocena: {rating}/10)")
                    
                    choice = self.get_user_input("\nWybierz numer filmu (0-{0}): ".format(len(rated_movies)), int)
                    
                    if choice == 0:
                        continue
                    elif 1 <= choice <= len(rated_movies):
                        selected_movie, current_rating = rated_movies[choice - 1]
                        print(f"\nZmieniasz ocenę filmu: {selected_movie.title}")
                        
                        # Użyj nowej funkcji do zmiany oceny
                        self.user.change_movie_rating(selected_movie.movie_id)
                        # Aktualizuj rekomender po zmianie oceny
                        self.recommender = create_recommender(self.user)
                    else:
                        print("Nieprawidłowy wybór!")
                
            elif option == 4:
                return  # Wraca do głównego menu
                
            else:
                print("\nNieprawidłowa opcja!") # Wyświetla błąd innej opcji niz ta w menu.
            
          
    # Funkcja do obslugi akcji wykonywanych na filmach.            
    def handle_movie_menu(self):
        while True:
            self.display_movie_menu() # Wyświetla menu akcji na filmach
            option = self.get_user_input("\n Wybierz opcję: ", int) # Pobiera zapytanie o wybór opcji od uzytkownika
            
            if option == 1: # Dodaje film do listy obejrzanych filmów.
                    add_movie_id = self.get_user_input("\nPodaj id filmu, zeby dodac do film do histori oglądania: ", int)
                        
                    self.user.add_to_history(add_movie_id)
                    print(f"\nDodano film o ID {add_movie_id} do listy obejrzanych filmów.")

            elif option == 2:
                self.handle_ratings_menu()
                
            elif option == 3:
                self.handle_movie_serach() # Wywołuje funkcje do wyszukiwania filmów
                
            elif option == 4:
                return  # Wraca do głównego menu
                
            else:
                print("\nNieprawidłowa opcja!") # Wyświetla błąd innej opcji niz ta w menu.
                
    # Funkcja do wyszukiwania filmów.
    def handle_movie_serach(self):
        user_movie = self.get_user_input("Podaj nazwę filmu: ", str) # Pobiera od uzytkownika nazwe filmu jako string
        movies = search_movies(user_movie) # Wykorzystuje funkcję do wyszukiwania filmów, która znajduje się w api.py
        
        if movies:
            print(f"\nZnaleziono {len(movies)} filmów, wyświetlam 5 odpowiadających wyszukiwaniu: '{user_movie}'\n")
                    
            for i, movie_data in enumerate(movies[:5], 1):
                movie = Movie.from_api_data(movie_data)
                print(f"{i}. {movie}")          
            
        else:
            print(f"\nNie znaleziono wyników dla: {user_movie}")


    # Funkcja zarządzjąca działaniem programu.
    def run(self):
        while True:
            self.display_main_menu() # Wyświetla główne menu.
            option = self.get_user_input("\nWybierz opcję: ", int) # Pobiera zapytanie o wybór opcji od uzytkownika.
                
            if option == 1:
                self.handle_movie_serach() # Wywołuje funkcję do wyszukiwania filmów.
                self.handle_movie_menu() # Wywołuje funkcje do obsługi akcji wykonywanych na filmach.
                self.user.save_user_data() # Zapisuje dane do pliku json.
                    
            elif option == 2:
                self.user.load_watch_history() # Wyświetla historię obejrzanych filmów.
                # Brak break - program kontynuuje pętlę i wraca do menu głównego
                    
            elif option == 3:
                self.handle_ratings_menu() # Wyświetla menu oceniania filmów.    
                
            elif option == 4:
                self.handle_recommendations_menu() # Wyświetla menu rekomendacji
                
            elif option == 5:
                self.show_rewatch_recommendations() # Pokazuje filmy do ponownego obejrzenia
                
            elif option == 6:
                self.show_user_statistics() # Pokazuje statystyki użytkownika
                
            elif option == 7:
                self.handle_similar_movies() # Obsługuje wyszukiwanie podobnych filmów
                
            elif option == 8: # Zamyka działanie programu
                self.user.save_user_data()
                print("Do zobaczenie! :)")
                break
                        
            else:
                print("\nNieprawidłowa opcja!")
                
                
if __name__ == "__main__":
    app = MovieRecomenderApp()
    app.run()
    