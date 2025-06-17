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
            #todo skrypt do oceniania filmow
            
            self.handle_movie_menu()
            
        elif option == 3:
            self.handle_movie_serach()
            self.handle_movie_menu()
            
        elif option == 4:
            self.run()
                
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
            option = self.get_user_input("\nWybierz opcję: ", int) # Pobiera zapytanie o wybor opcji od uzytkownika.
                
            if option == 1:
                self.handle_movie_serach()
                self.handle_movie_menu()
                break
                
                    
            # elif option == 2:

                    
            # elif option == 3:
                
                
            # elif option == 4:
                
                
            elif option == 5: # Zamyka działanie programu
                self.user.save_user_data()
                print("Do zobaczenie! :)")
                break
                        
            else:
                print("\nNieprawidłowa opcja!")
                
                
if __name__ == "__main__":
    app = MovieRecomenderApp()
    app.run()
            

        



    
# def movie_menu():
#     while True:
#         print("\n --- MENU AKCJI ---")
#         print("1. Dodaj film do historii ogladania ")#todo dodac opcje ocenienia filmu po dodaniu do obejrzanych oraz mozliwe wyswietlnie historie obejrznych filmow.
#         print("2. Ponownie wyszukaj film")
#         print("3. Cofnij sie do menu głównego")
#         print("4. Zamknij program")
            
#         option = question()
                    
#         if option == 1:
#             try:
#                 add_movie_id_input = int(input("\nPodaj id filmu, zeby dodac do film do histori oglądania: "))
                    
#                 user.add_to_history(add_movie_id_input)
#                 print(f"\nDodano film o ID {add_movie_id_input} do listy obejrzanych filmów.")
#             except ValueError:
#                 print("\nTo nie jest ID. Podaj ID filmu, zeby dodać go do listy obejrzanych filmów.")
                        
#         elif option == 2:
#             movie_menu_action()
                
#         elif option == 3:
#             main_menu_action()
                
#         elif option == 4:
#             close()
                
#         else:
#             print("\nOpcja nie istnieje!")


# def movie_menu_action():
#     user_movie = input("Podaj nazwę filmu: ")
#     movies = search_movies(user_movie)
        
#     if movies:
#         print(f"\nZnaleziono {len(movies)} filmów, wyświetlam 5 odpowiadających wyszukiwaniu: '{user_movie}'\n")
            
#         for i, movie_data in enumerate(movies[:5], 1):
#             movie = Movie.from_api_data(movie_data)
#             print(f"{i}. {movie}")        
            
#         while True:
#             user_question = input("\nChcesz wykonać jakąś akcję na filmie z listy lub wyszukać ponownie? (tak/nie): ")
        
#             if user_question in ['tak']:
#                 movie_menu()
            
#             elif user_question in ['nie']:
#                 main_menu_action()
                
#             else:
#                 print("\nNie poprawna opcja, wpisz (tak/nie)")
                
                
#     else:
#         print(f"\nNie znaleziono wyników dla: {user_movie}")

  
# def main_menu_action():  
#     while True:
#         menu()
#         option = question()
            
#         if option == 1:
#             movie_menu_action()
                
#         elif option == 2:
#             user.load_watch_history()
                
#         elif option == 3:
#             close()
                    
#         else:
#             print("\nOpcja nie istnieje.")


# main_menu_action()