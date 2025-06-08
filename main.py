"""
Główny plik programu System Rekomendacji Filmów

Odpowiada za:
- Interfejs użytkownika (menu, wyświetlanie wyników)
- Główną pętlę programu
- Integrację wszystkich modułów systemu
"""
from api import search_movies
from models import User

def menu():
    print()
    print("MENU")
    print("1. Wyszukaj film")
    print("2. Wyświetl rekomendacje")
    print("3. Wyjście")
    print()
    
user = User(1, "Kacper")
    
while True:
    menu()
    
    try:
        selected_option = int(input("Wpisz numer opcji, zeby wybrac: "))
    except ValueError:
        print()
        print("Żeby wybrać opcję wpisz jej numer!")
        continue
    
    if selected_option == 1:
        user_movie = input("Podaj nazwę filmu: ")
        
        movies = search_movies(user_movie)
    elif selected_option == 2:
        display_recommendations()
    elif selected_option == 3:
        user.save_user_data()
        print("Do zobaczenia :)")
        exit()
    else:
        print()
        print("Nie ma takiej opcji.")
