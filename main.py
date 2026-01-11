import sys
# Importujemy niezbedne klasy z modulu QtWidgets
from PyQt5 . QtWidgets import QApplication , QWidget , QLabel
# 1. Tworzymy instancje aplikacji ( wymagane !)
app = QApplication ( sys . argv )
# 2. Tworzymy glowne okno ( pusty widzet )
window = QWidget ()
window . setWindowTitle ('Moja pierwsza aplikacja PyQt ')
window . setGeometry (100 , 100 , 400 , 200) # x, y, szer , wys
# 3. Dodajemy etykiete ( tekst ) do okna
# parent = window sprawia , ze etykieta jest wewnatrz okna
label = QLabel ('Witaj w swiecie PyQt !', parent = window )
label . move (120 , 80) # Ustawiamy pozycje etykiety
# 4. Wyswietlamy okno
window . show ()
# 5. Uruchamiamy petle zdarzen ( nieskonczona petla )
sys . exit ( app . exec_ () )
