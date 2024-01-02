import PySimpleGUI as sg
import pandas as pd
import sys
from typing import List

# Funkcja do wczytywania bazy danych leków z pliku
def wczytaj_baze_lekow():
    try:
        baza_lekow = pd.read_csv('baza.csv', sep=';')
        #Przekształcenie kolumn Skladniki i Kolizje ze stringa na tablicę stringów oddzieloną znakami ,
        baza_lekow['Skladniki'] = baza_lekow['Skladniki'].str.split(',').apply(lambda x: [s.strip() for s in x] if isinstance(x, list) else [])
        baza_lekow['Kolizje'] = baza_lekow['Kolizje'].str.split(',').apply(lambda x: [s.strip() for s in x] if isinstance(x, list) else [])
        return baza_lekow
    except:
        print("Nie znaleziono bazy danych z lekami")
        sys.exit(1)

# Funkcja do wczytywania apteczki pacjenta z pliku
def wczytaj_apteczke():
    apteczka: List[str] = []
    try:
        with open('.apteczka.csv', 'r') as apteczka_csv:
            for linia in apteczka_csv:
                for element in linia.strip().split(';'):
                    if element.strip():
                        apteczka.append(str(element))
        apteczka_csv.close()
        return apteczka
    except:
        return []

# Funkcja do zapisywania apteczki do pliku
def zapisz_apteczke(apteczka: List[str]):
    with open('.apteczka.csv', 'w') as apteczka_csv:
        for lek in apteczka:
            apteczka_csv.write(str(lek) + ';' + '\n')
    print("Zawartość apteczki:", apteczka)
    apteczka_csv.close()

# Funkcja do sprawdzania kolizji między lekami
def sprawdz_kolizje(baza_lekow, apteczka):
    roboczy_df = pd.DataFrame(columns=['Nazwa', 'Skladniki', 'Kolizje'])
    for lek in apteczka:
        wiersz = baza_lekow[baza_lekow['Nazwa'] == lek].copy()
        wiersz.reset_index(drop=True, inplace=True)
        roboczy_df = pd.concat([roboczy_df, wiersz], ignore_index=True)
    komunikaty_kolizji = []

    for i, lek1 in roboczy_df.iterrows():
        for j, lek2 in roboczy_df.iterrows():
            if i != j:
                skladniki_leku1 = set(lek1['Skladniki'])
                kolizje_leku2 = set(lek2['Kolizje'])
                kolizje_skladnikow = skladniki_leku1.intersection(kolizje_leku2)
                if kolizje_skladnikow:
                    komunikat = f"Kolizja: {lek1['Nazwa']} i {lek2['Nazwa']} - Składniki: {', '.join(kolizje_skladnikow)}"
                    komunikaty_kolizji.append(komunikat)

    return komunikaty_kolizji

# GUI aplikacji
apteczka: List[str] = wczytaj_apteczke()  # Inicjalizacja listy leków pacjenta
print(apteczka)
baza_lekow: pd.DateOffset = wczytaj_baze_lekow()  # Wczytanie bazy leków

layout = [
    [sg.Text('Dodaj lek do swojej listy:')],
    [sg.InputText(key='nowy_lek', size=(72,1)), sg.Button('Dodaj')],
    [sg.Listbox(values=apteczka, size=(36, 15), key='lista_lekow'), sg.Text('', size=(36, 15), key='komunikat')],
    [sg.Button('Usuń zaznaczony lek', size=(36,1)), sg.Button('Sprawdź kolizje', size=(36,1))],
]

window = sg.Window('Wykrywanie kolizji leków', layout, size=(600, 370))

# Główna pętla aplikacji
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        zapisz_apteczke(apteczka)  # Zapisz listę leków do pliku przed zamknięciem
        break

    if event == 'Dodaj':
        nowy_lek = values['nowy_lek'].strip()
        if nowy_lek:
            if nowy_lek in baza_lekow['Nazwa'].values:
                if nowy_lek not in apteczka:
                    apteczka.append(nowy_lek)
                    window['lista_lekow'].update(values=apteczka)
                    zapisz_apteczke(apteczka)  # Zapisz apteczkę do pliku po dodaniu nowego leku
                    window['komunikat'].update('Pomyślnie dodano '+ nowy_lek + ' do apteczki')
                    window['nowy_lek'].update('')
                else:
                    window['komunikat'].update('Lek, który chcesz dodać do apteczki, już się w niej znajduje')
            else:
                window['komunikat'].update('Leku, który chcesz dodać, nie ma w naszej bazie')
        else:
            window['komunikat'].update('Aby dodać lek, musisz wprowadzić jego nazwę.')

    if event == 'Usuń zaznaczony lek':
        wybrane_leki = values['lista_lekow']
        if wybrane_leki:
            lek_do_usuniecia = wybrane_leki[0]
            apteczka.remove(lek_do_usuniecia)
            window['lista_lekow'].update(values=apteczka)
            zapisz_apteczke(apteczka)  # Zapisz listę leków do pliku po usunięciu leku

    if event == 'Sprawdź kolizje':
        komunikaty_kolizji = sprawdz_kolizje(baza_lekow, apteczka)
        if komunikaty_kolizji:
            sg.popup("\n".join(komunikaty_kolizji), title='Komunikat kolizji')
        else:
            sg.popup("Nie znaleziono kolizji", title='Komunikat')

window.close()

