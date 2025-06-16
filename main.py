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

user = User(1, "Kacper")

def question():
    try:
        selected_option = int(input("\nWpisz numer opcji z menu, zeby wybrac: "))
        return selected_option
            
    except ValueError:
        print("\nNie poprawny znak. Wpisz numer z menu, zeby wybrac akcję.")
        return None
        

def menu():
    print("\n--- MENU ---")
    print("1. Wyszukaj film")
    print("2. Zobacz listę obejrzanych filmów")
    print("3. Zamknij program")


def close():
    user.save_user_data()
    print("Do zobaczenia :)")
    exit()
    
def movie_menu():
    while True:
        print("\n --- MENU AKCJI ---")
        print("1. Dodaj film do historii ogladania ")#todo dodac opcje ocenienia filmu po dodaniu do obejrzanych oraz mozliwe wyswietlnie historie obejrznych filmow.
        print("2. Ponownie wyszukaj film")
        print("3. Cofnij sie do menu głównego")
        print("4. Zamknij program")
            
        option = question()
                    
        if option == 1:
            try:
                add_movie_id_input = int(input("\nPodaj id filmu, zeby dodac do film do histori oglądania: "))
                    
                user.add_to_history(add_movie_id_input)
                print(f"\nDodano film o ID {add_movie_id_input} do listy obejrzanych filmów.")
            except ValueError:
                print("\nTo nie jest ID. Podaj ID filmu, zeby dodać go do listy obejrzanych filmów.")
                        
        elif option == 2:
            movie_menu_action()
                
        elif option == 3:
            main_menu_action()
                
        elif option == 4:
            close()
                
        else:
            print("\nOpcja nie istnieje!")


def movie_menu_action():
    user_movie = input("Podaj nazwę filmu: ")
    movies = search_movies(user_movie)
        
    if movies:
        print(f"\nZnaleziono {len(movies)} filmów, wyświetlam 5 odpowiadających wyszukiwaniu: '{user_movie}'\n")
            
        for i, movie_data in enumerate(movies[:5], 1):
            movie = Movie.from_api_data(movie_data)
            print(f"{i}. {movie}")        
            
        while True:
            user_question = input("\nChcesz wykonać jakąś akcję na filmie z listy lub wyszukać ponownie? (tak/nie): ")
        
            if user_question in ['tak']:
                movie_menu()
            
            elif user_question in ['nie']:
                main_menu_action()
                
            else:
                print("\nNie poprawna opcja, wpisz (tak/nie)")
                
                
    else:
        print(f"\nNie znaleziono wyników dla: {user_movie}")

  
def main_menu_action():  
    while True:
        menu()
        option = question()
            
        if option == 1:
            movie_menu_action()
                
        elif option == 2:
            user.load_watch_history()
                
        elif option == 3:
            close()
                    
        else:
            print("\nOpcja nie istnieje.")


main_menu_action()