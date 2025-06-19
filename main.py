"""
Główny plik programu System Rekomendacji Filmów

Odpowiada za:
- Interfejs użytkownika (menu, wyświetlanie wyników)
- Główną pętlę programu
- Integrację wszystkich modułów systemu
"""
from api import search_movies
from models import User
from models import Movie


class MovieRecomenderApp:
    def __init__(self):
        self.user = User(1, "Kacper")
    
    
    # Funkcje do wyświetalnia menu.
    def display_main_menu(self):
        print("\n--- MENU ---")
        print("1. Wyszukaj film")
        print("2. Zobacz listę obejrzanych filmów")
        print("3. Zarządzaj ocenami")
        print("4. Sprawdź rekomendowane filmy")
        print("5. Zamknij program")
        
        
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
        print("3. Wróć do menu głównego")
        
        
    # Pobieranie danych od uzytkownika    
    def get_user_input(self, prompt, type_cast=int):
        while True:
            try:
                return type_cast(input(prompt))
            except ValueError:
                print(f"\nNieprawidłowa warość! Wprowadź {type_cast.__name__}.")
                
                
    # Funkcja do obsługi ocen na filmach
    def handle_ratings_menu(self):
        self.display_ratings_menu() # Wyświetla menu ocen.
        option = self.get_user_input("\n Wybierz opcję: ", int) # Pobiera zapytanie o wybór opcji od uzytkownika
        
        if option == 1:
            movie_id = self.get_user_input("\nPodaj ID filmu, który chcesz ocenić: ", int) # Pobiera ID filmu do oceny od uzytkownika
            self.user.rate_movie(movie_id) # Wywołuje funkcję oceniania filmów z models.py
            self.handle_ratings_menu() # Uruchamia ponownie funkcję, zeby program sie nie wyłączył.
            
        elif option == 2:
            self.user.load_ratings()
            self.handle_ratings_menu() # Uruchamia ponownie funkcję, zeby program sie nie wyłączył.
            
        elif option == 3:
            self.run()
            
        else:
            print("\nNieprawidłowa opcja!") # Wyświetla błąd innej opcji niz ta w menu.
            self.handle_ratings_menu() # Wywołuje ponownie funkcję
            
          
    # Funkcja do obslugi akcji wykonywanych na filmach.            
    def handle_movie_menu(self):
        self.display_movie_menu() # Wyświetla menu akcji na filmach
        option = self.get_user_input("\n Wybierz opcję: ", int) # Pobiera zapytanie o wybór opcji od uzytkownika
        
        if option == 1: # Dodaje film do listy obejrzanych filmów.
                add_movie_id = self.get_user_input("\nPodaj id filmu, zeby dodac do film do histori oglądania: ", int)
                    
                self.user.add_to_history(add_movie_id)
                print(f"\nDodano film o ID {add_movie_id} do listy obejrzanych filmów.")
                self.handle_movie_menu()

        elif option == 2:
            self.handle_ratings_menu()
            
            self.handle_movie_menu() # Wyświetla ponownie menu akcji na filmach
            
        elif option == 3:
            self.handle_movie_serach() # Wywołuje funkcje do wyszukiwania filmów
            self.handle_movie_menu() # Wyświetla ponownie menu akcji na filmach
            
        elif option == 4:
            self.run() # Wraca do menu głównego wywyłójąc jej funkcję
            
        else:
            print("\nNieprawidłowa opcja!") # Wyświetla błąd innej opcji niz ta w menu.
            self.handle_movie_menu() # Wywołuje ponownie funkcję
                
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
                break
                
                    
            elif option == 2:
                self.user.load_watch_history() # Wyświetla historię obejrzanych filmów.
                    
            elif option == 3:
                self.handle_ratings_menu() # Wyświetla menu oceniania filmów.    
                break
                
            # elif option == 4: #todo Podpiąć tutaj algorytm rekomendacji filmów
                
                
            elif option == 5: # Zamyka działanie programu
                self.user.save_user_data()
                print("Do zobaczenie! :)")
                break
                        
            else:
                print("\nNieprawidłowa opcja!")
                
                
if __name__ == "__main__":
    app = MovieRecomenderApp()
    app.run()
    