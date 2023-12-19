# Bazy danych
## Baza leków
Nazwa pliku z bazą: .baza.csv
Separator: ';', ',' zarezerwowany na separator przy listach składników i kolizji

### Przykład:
Nazwa;Skladniki;Kolizje
lek_1;a, b, c;d
lek_2;a, b, d;e, f
lek_3;f;a, b, c, d, e

Wokół ; nie może być spacji, zwłaszcza przy nagłówkach. Inaczej wszystko się popsuje. 

## Apteczka (lista leków, które obecnie przyjmuje użytkownik, zmieniłem nazwę na apteczka bo jest krótsza i imo bardziej intuicyjna)
Nazwa pliku z apteczką: .apteczka.csv
Separator: ;

### Przykład
lek_1;
lek_2;

Nie przechowujemy tu kolizji ani info o składnikach. Nazwy muszą przystawać do tych, które są w bazie danych. 

Wczytywanie obu baz jest proste jak cep i nie chce mi się ich tu opisywać, zwłaszcza że działają :)

# Wyszukiwarka kolizji

Lek może pozostawać w konflikcie z własną substancją aktywną (np. na apapie pisze, że nie wolno stosować z innymi lekami zawierającymi paracetamol). 

Wyszukiwanie kolizji działa tak, że:
- iterujemy po lekach, które użytkownik ma w apteczce. 
- informację wyświetlamy w taki sposób, że piszemy który lek (np. A) wchodzi w interakcję z jakim lekiem i w nawiasie podajemy z powodu jakiej susbtancji. Lek nie może być w kolizji sam z sobą. Np.

Ibum koliduje z Nurofenem (nazwa_substancji)
Nurofen koliduje z Ibumem (nazwa_substancji)

OLAF jak będziesz robić bazę to przejrzyj, czy mozna powiedzieć, że relacja jest symetryczna, czy nie (tj. czy zawsze/zazwyczaj jest tak, że jak A koliduje z B poprzez subs. x, to B z A poprzez x. Wtedy można wyrzucić połowę sprawdzeń). 