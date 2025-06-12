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

def menu():
    print()
    print(" --- MENU ---")
    print("1. Wyszukaj film")
    print("2. Zobacz listę obejrzanych filmów")
    print("3. Wyjście")
    print()

def close():
        user.save_user_data()
        print("Do zobaczenia :)")
        exit()

def movie_menu_action():
    def movie_menu():
        print("\n --- MENU AKCJI ---")
        print("1. Dodać film do historii oglądania ")
        print("2. Ponownie wyszukać film")
        print("3. Wyjść")
    
    user_movie = input("Podaj nazwę filmu: ")
    movies = search_movies(user_movie)
        
    if movies:
        print(f"\nZnaleziono {len(movies)} filmów, wyświetlam 5 odpowiadających wyszukiwaniu: '{user_movie}'\n")
            
        for i, movie_data in enumerate(movies[:5], 1):
            movie = Movie.from_api_data(movie_data)
            print(f"{i}. {movie}")        
            
        user_question = input("\nChcesz wykonać jakąś akcję na filmie z listy? (tak/nie): ")
        if not user_question in ['nie']:
            movie_menu()
            
        user_question_2 = input("\nChcesz zamknąć program? (tak/nie): ")
        if not user_question_2 in ['nie']:
            close()
                
    else:
        print(f"\nNie znaleziono wyników dla: {user_movie}")

    
while True:
    menu()
    
    try:
        selected_option = int(input("Wpisz numer opcji, zeby wybrac: "))
        
    except ValueError:
        print("\nŻeby wybrać opcję wpisz jej numer!")
        continue
    
    
    if selected_option == 1:
        movie_menu_action()
            
    elif selected_option == 2:
        user.load_watch_history()
            
    elif selected_option == 3:
        close()
                
    else:
        print()
        print("Nie ma takiej opcji.")
