import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont

# --- KLASA KOMORA SILNIKA ---
class Komora_silnika:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0
        self.poziom_roboczy = 0.0
        self.ustawienie_tloka_blok = 0.0

    def dodaj_pare(self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_pare(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc
        if self.h_pary > 28:
            self.poziom_roboczy = (self.h_pary-28)/(self.height-28)
        else:
            self.poziom_roboczy = 0
        
    def ustaw_tlok_blok(self, wartosc):
        self.ustawienie_tloka_blok = wartosc

    def czy_pusty(self):
        return self.aktualna_ilosc <= 0 and self.aktualna_ilosc <= 0

    def czy_pelny(self):
        return self.aktualna_ilosc >= self.pojemnosc and self.aktualna_ilosc >= 0
    
    def punkt_wlotu(self):
        return (self.x, self.y + 5)

    def punkt_gora_srodek(self):
        return (self.x + self.width / 2, self.y)

    def punkt_dol_srodek(self):
        return (self.x + self.width / 2, self.y + self.height)
    
    def punkt_srodek_tloka(self):
        if self.h_pary > 28: return (int(self.x+3+((self.width-6)/2)), int(self.y+self.h_pary+10))
        else: return (int(self.x+3+((self.width-6)/2)), int(self.y+28+10))
    
    def punkt_polaczenie_korbowod(self):
        return int(self.x+3+self.width-40+20+40+(self.ustawienie_tloka_blok*20)), int(self.y+3+10)

    def draw(self, painter):
        # 1. Rysowanie pary
        self.h_pary = self.height * self.poziom
        if self.poziom > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(200, 200, 200, 120))
            painter.drawRect(int(self.x+3), int(self.y), int(self.width - 6), int(self.h_pary))

        # 2. Rysowanie tłoku głównego
        pen = QPen(Qt.white, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.white)
        if self.h_pary > 28:
            painter.drawRect(int(self.x+3), int(self.y+self.h_pary), int(self.width - 6), 20)
        else:
            painter.drawRect(int(self.x+3), int(self.y+28), int(self.width - 6), 20)

        # 3. Rysowanie obrysu
        pen = QPen(Qt.white, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(int(self.x), int(self.y), int(self.x), int(self.y) + int(self.height+20))
        painter.drawLine(int(self.x), int(self.y), int(self.x) + int(self.width) - 40, int(self.y))
        painter.drawLine(int(self.x) + int(self.width) - 20, int(self.y), int(self.x) + int(self.width), int(self.y))
        painter.drawLine(int(self.x) + int(self.width), int(self.y), int(self.x) + int(self.width), int(self.y) + int(self.height) + 20)
        painter.drawLine(int(self.x) + int(self.width), int(self.y) + int(self.height) + 20, int(self.x) + int(self.width) - 20, int(self.y) + int(self.height) + 20)
        painter.drawLine(int(self.x), int(self.y) + int(self.height) + 20, int(self.x) + 20, int(self.y) + int(self.height) + 20)

        # 4. Rysowanie tłoku blokującego wejśćie/wyjście
        painter.save()
        
        xb = self.ustawienie_tloka_blok * 20
        painter.translate(xb, 0)
        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.white)
        painter.drawRect(int(self.x+3), int(self.y+3), int(self.width-40), 20)
        painter.drawRect(int(self.x+3+self.width-40), int(self.y+9), 20, 8)
        painter.drawRect(int(self.x+3+self.width-40+20), int(self.y+3), 40, 20)

        painter.restore()

        # 5. Podpis nad zbiornikiem
        painter.setPen(Qt.white)
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)
        painter.drawText(int(self.x), int(self.y - 25), self.nazwa)
        painter.drawText(int(self.x), int(self.y - 10), str(int(self.poziom*100))+"% pary")