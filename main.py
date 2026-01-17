import sys
import math
from rura import Rura
from zbiornik import Zbiornik
from komorasilnika import Komora_silnika
from kolo import Kolo
from kociol import Kociol
from korbowod import Korbowod
from korbowod_przymocowany import KorbowodPrzymocowany
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
WIDTH = 900
HEIGHT = 600
KOCIOL_POSX = WIDTH/5
KOCIOL_POSY = 140+(HEIGHT/3)
ZBIORNIK_POSX = WIDTH/5
ZBIORNIK_POSY = HEIGHT/3
KOMORA_POSX = WIDTH*45/100
KOMORA_POSY = HEIGHT/3
PREDKOSC_SYMULACJI = 1

# --- GŁÓWNA KLASA SYMULACJI ---
class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silnik Parowy")
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

        # --- Konifugracja Korbowod ---
        self.korbowod1 = Korbowod(self.k1.punkt_srodek_tloka, self.kolo.punkt_zaczepienia)
        self.korbowod2 = KorbowodPrzymocowany(int(KOMORA_POSX+200), int(KOMORA_POSY+43))
        self.korbowod3 = Korbowod(self.kolo.punkt_zaczepienia, self.korbowod2.punkt_koniec)
        self.korbowod4 = Korbowod(self.korbowod2.punkt_start, self.k1.punkt_polaczenie_korbowod)
        self.korbowod = [self.korbowod1, self.korbowod2, self.korbowod3, self.korbowod4]

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
        mnoznik = (math.sqrt(mnoznik)/5)*PREDKOSC_SYMULACJI
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
        pressure_modifier = 1.004**abs(self.z1.temperatura-100)
        if not self.k1.czy_pelny() and self.faza_doplywu :
            ilosc = self.z1.usun_pare(self.flow_speed*pressure_modifier)
            if ilosc > 0:
                self.k1.dodaj_pare(ilosc)
                self.kolo.ustaw_kat(-self.k1.poziom_roboczy*180)
                plynie_1 = 2
        elif self.k1.czy_pelny():
            self.faza_doplywu = False
            plynie_1 = 0
        if self.faza_doplywu == False:
            ilosc = self.k1.usun_pare(self.flow_speed*pressure_modifier)
            self.kolo.ustaw_kat(self.k1.poziom_roboczy*180)
            if self.k1.czy_pusty():
                self.faza_doplywu = True
        self.r1.ustaw_przeplyw(plynie_1)

        #Kolo -> korbowod przymocowany
        full_kat = 60
        if self.kolo.kat <= 60 and self.kolo.kat > -120:
            norm = abs(self.kolo.kat - 60)/180
            kat = norm*full_kat - full_kat/2
        else:
            if self.kolo.kat < 0:
                norm = abs(self.kolo.kat + 120)/180
            else:
                norm = abs(60+(180-self.kolo.kat))/180
            kat = -norm*full_kat + full_kat/2
        self.korbowod2.ustaw_kat(kat)

        #korbowod przymocowany -> tlok wpuszczajacy/wypuszczajacy pare
        if not (self.kolo.kat <= 60 and self.kolo.kat > -120):
            norm = 1-norm
        self.k1.ustaw_tlok_blok(norm)

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
        for korb in self.korbowod:
            korb.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec())