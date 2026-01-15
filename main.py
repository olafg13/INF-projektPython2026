import sys
import math
from rura import Rura
from zbiornik import Zbiornik
from komorasilnika import Komora_silnika
from kolo import Kolo
from kociol import Kociol
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
WIDTH = 900
HEIGHT = 600
KOCIOL_POSX = WIDTH/3
KOCIOL_POSY = 140+(HEIGHT/3)
ZBIORNIK_POSX = WIDTH/3
ZBIORNIK_POSY = HEIGHT/3
KOMORA_POSX = WIDTH*2/3
KOMORA_POSY = HEIGHT/3
PREDKOSC_SYMULACJI = 10

# --- GŁÓWNA KLASA SYMULACJI ---
class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zbiorniki")
        self.setFixedSize(WIDTH, HEIGHT)
        self.setStyleSheet("background-color: #2b2b2b;")

        # --- Konfiguracja kotła ---
        self.kociol = Kociol(KOCIOL_POSX, KOCIOL_POSY, nazwa="Kocioł")

        # --- Konfiguracja Komór silnika ---
        self.k1 = Komora_silnika(KOMORA_POSX, KOMORA_POSY, nazwa="Komora")
        self.k1.aktualizuj_poziom

        self.komory = [self.k1]

        # --- Konfiguracja Zbiorników ---
        self.z1 = Zbiornik(ZBIORNIK_POSX, ZBIORNIK_POSY, nazwa="Zbiornik 1")
        self.z1.dodaj_ciecz(50)
        self.z1.aktualizuj_poziom()

        self.zbiorniki = [self.z1]

        # --- Konfiguracja Rur ---
        p_start = self.z1.punkt_gora_srodek()
        p_koniec = self.k1.punkt_wlotu()
        mid_y = (p_start[1] + p_koniec[1]) / 2
        mid_x = (p_start[0] + p_koniec[0]) / 2
        
        self.r1 = Rura([p_start, (p_start[0], mid_y-15), (mid_x, mid_y-15), (mid_x, p_koniec[1]), p_koniec])
    
        self.rury = [self.r1] 
        
        # --- Konfiguracja Kol ---
        self.kolo = Kolo(int(KOMORA_POSX+self.k1.width/2), int(self.k1.y+200), nazwa="Kolo")

        # --- Przyciski ---
        self.btn = QPushButton("START", self)
        self.btn.setGeometry(30, 520, 100, 50)
        self.btn.setStyleSheet("background-color: yellow; color: black; font-size: 14px")
        self.btn.clicked.connect(self.przelacz_symulacje)

        # --- Suwaki ---
        self.suwak = QSlider(Qt.Horizontal, self)
        self.suwak.setGeometry(int(KOCIOL_POSX), int(KOCIOL_POSY)+200, 100, 20)
        self.suwak.setMinimum(0)
        self.suwak.setMaximum(500)
        self.suwak.valueChanged.connect(self.kociol.ustaw_temp)

        # --- Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)
        self.running = False
        self.flow_speed = 5*PREDKOSC_SYMULACJI

        self.faza_doplywu = True

    def przelacz_symulacje(self):
        if self.running:
            self.timer.stop()
            self.btn.setText("START")
        else:
            self.timer.start(20)
            self.btn.setText("STOP")
        self.running = not self.running

    def logika_przeplywu(self):
        #kociol -> Z1 TEMP
        if self.kociol.temperatura > self.z1.temperatura:
            przyrost = ((self.kociol.temperatura - self.z1.temperatura)/500)*PREDKOSC_SYMULACJI
            self.z1.dodaj_temp(przyrost)

        #Z1 -> WODA -> PARA -> WODA
        mnoznik = abs(self.z1.temperatura-100)
        mnoznik = (math.sqrt(mnoznik)/10)*PREDKOSC_SYMULACJI
        if self.z1.temperatura >= 100:
            usunieto = self.z1.usun_ciecz(0.001*mnoznik)
            if usunieto != 0:
                self.z1.dodaj_pare(1600*usunieto)
        if self.z1.temperatura < 100:
            usunieto = self.z1.usun_pare(1.6*mnoznik)
            if usunieto != 0:
                self.z1.dodaj_ciecz(usunieto/1600)

        #Z1 -> TEMP SPADEK
        if self.z1.temperatura > 0 and self.z1.temperatura > self.kociol.temperatura:
            spadek = ((self.z1.temperatura-self.kociol.temperatura)/300)*PREDKOSC_SYMULACJI
            self.z1.usun_temp(spadek)
        

        # Z1 -> K1 + obrot kola
        plynie_1 = 0
        if not self.k1.czy_pelny() and self.faza_doplywu :
            ilosc = self.z1.usun_pare(self.flow_speed)
            if ilosc > 0:
                self.k1.dodaj_pare(ilosc)
                self.kolo.usun_kat((ilosc/self.k1.pojemnosc)*180)
                plynie_1 = 2
        elif self.k1.czy_pelny():
            self.faza_doplywu = False
            self.kolo.ustaw_kat(180)
            plynie_1 = 0
        if self.faza_doplywu == False:
            ilosc = self.k1.usun_pare(self.flow_speed)
            self.kolo.usun_kat((ilosc/self.k1.pojemnosc)*180)
            if self.k1.czy_pusty():
                self.faza_doplywu = True

        self.r1.ustaw_przeplyw(plynie_1)

        
        """
        # Z2 -> Z3
        plynie_2 = False
        if self.z2.aktualna_ilosc > 5.0 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(self.flow_speed)
            self.z3.dodaj_ciecz(ilosc)
            plynie_2 = True
        self.rura2.ustaw_przeplyw(plynie_2)

        """
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # 1. Rysowanie elementów symulacji
        for r in self.rury:
            r.draw(p)
        for z in self.zbiorniki:
            z.draw(p)
        self.kolo.draw(p)
        for k in self.komory:
            k.draw(p)
        self.kociol.draw(p)
        x1, y1 = self.k1.punkt_srodek_tloka()
        x2, y2 = self.kolo.punkt_zaczepienia()
        pen = QPen(Qt.gray, 6)
        p.setPen(pen)
        p.drawLine(x1,y1,x2,y2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec())