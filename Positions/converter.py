def przelicz_kat_na_duty_cycle(kat):
    """
    Przelicza wartość kąta (-90 do 90 stopni) na wartość duty cycle (500 do 2500).

    Argumenty:
        kat (int): Kąt w stopniach (-90 do 90).

    Zwraca:
        int: Wartość duty cycle (500 do 2500).
    """
    min_kat = -90
    max_kat = 90
    min_duty_cycle = 500
    max_duty_cycle = 2500

    # Upewnij się, że kąt jest w dozwolonym zakresie
    kat = max(min_kat, min(max_kat, kat))

    duty_cycle = int(((kat - min_kat) / (max_kat - min_kat)) * \
                     (max_duty_cycle - min_duty_cycle) + min_duty_cycle)
    return duty_cycle

def konwertuj_serwa(plik_wejsciowy, plik_wyjsciowy):
    """
    Wczytuje dane serw z pliku wejściowego, przelicza kąty na duty cycle
    i zapisuje zaktualizowane dane do pliku wyjściowego.

    Argumenty:
        plik_wejsciowy (str): Nazwa pliku do odczytu danych serw.
        plik_wyjsciowy (str): Nazwa pliku do zapisu przetworzonych danych.
    """
    linie = []
    try:
        with open(plik_wejsciowy, 'r') as plik:
            linie = plik.readlines()
    except FileNotFoundError:
        print(f"Błąd: Plik wejściowy '{plik_wejsciowy}' nie został znaleziony.")
        return

    przetworzone_linie = []
    for linia in linie:
        linia = linia.strip() # Usuń białe znaki, w tym znak nowej linii
        if linia: # Sprawdź, czy linia nie jest pusta
            czesci = linia.split()
            if len(czesci) == 2:
                try:
                    serwo_id = int(czesci[0])
                    kat = int(czesci[1])
                    duty_cycle = przelicz_kat_na_duty_cycle(kat)
                    przetworzone_linie.append(f"{serwo_id} {duty_cycle}\n")
                except ValueError:
                    print(f"Ostrzeżenie: Nieprawidłowy format wartości w linii '{linia}'. Pomijam.")
                    przetworzone_linie.append(linia + "\n") # Zachowaj oryginalną linię
            else:
                print(f"Ostrzeżenie: Nieprawidłowa liczba wartości w linii '{linia}'. Pomijam.")
                przetworzone_linie.append(linia + "\n") # Zachowaj oryginalną linię
        else:
            przetworzone_linie.append("\n") # Zachowaj puste linie

    try:
        with open(plik_wyjsciowy, 'w') as plik:
            plik.writelines(przetworzone_linie)
        print(f"Plik '{plik_wejsciowy}' został pomyślnie przetworzony.")
        print(f"Wyniki zapisano do pliku '{plik_wyjsciowy}'.")
    except IOError as e:
        print(f"Błąd podczas zapisu do pliku '{plik_wyjsciowy}': {e}")

# --- Główna część programu ---
if __name__ == "__main__":
    print("--- Konwerter kątów serw na duty cycle ---")

    # Wprowadź nazwę pliku wejściowego
    input_filename = input("Podaj nazwę pliku wejściowego (np. serwa_katy.txt): ")

    # Wprowadź nazwę pliku wyjściowego
    output_filename = input("Podaj nazwę pliku wyjściowego (np. serwa_dutycycle.txt): ")

    # Przykładowe dane wejściowe dla łatwego testowania
    # Utwórz plik wejściowy z danymi, jeśli nie istnieje
    try:
        with open(input_filename, 'x') as f:
            f.write("0 16\n")
            f.write("1 -35\n")
            f.write("2 0\n")
            f.write("3 90\n")
            f.write("4 66\n")
            f.write("5 7\n")
            f.write("6 0\n")
            f.write("7 -90\n")
        print(f"Utworzono przykładowy plik wejściowy '{input_filename}'.")
    except FileExistsError:
        print(f"Plik wejściowy '{input_filename}' już istnieje. Używam istniejącego pliku.")

    # Wykonaj konwersję
    konwertuj_serwa(input_filename, output_filename)

    print("\n--- Zawartość pliku wyjściowego po konwersji (jeśli istnieje) ---")
    try:
        with open(output_filename, 'r') as plik:
            print(plik.read())
    except FileNotFoundError:
        print(f"Plik wyjściowy '{output_filename}' nie znaleziony.")
    except Exception as e:
        print(f"Nie udało się odczytać pliku wyjściowego: {e}")