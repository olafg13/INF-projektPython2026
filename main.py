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
WIDTH = 1200
HEIGHT = 800
KOCIOL_POSX = 100
KOCIOL_POSY = 140+(HEIGHT/3)
ZBIORNIK1_POSX = 100
ZBIORNIK1_POSY = HEIGHT/3
KOMORA1_POSX = 325
KOMORA1_POSY = HEIGHT/2.5
KOMORA2_POSX = KOMORA1_POSX+315
KOMORA3_POSX = KOMORA2_POSX+315
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
        self.k1 = Komora_silnika(KOMORA1_POSX, KOMORA1_POSY, nazwa="Komora 1")
        
        self.k2 = Komora_silnika(KOMORA2_POSX, KOMORA1_POSY, nazwa="Komora 2")

        self.k3 = Komora_silnika(KOMORA3_POSX, KOMORA1_POSY, nazwa="Komora 3")

        self.k1.aktualizuj_poziom

        self.komory = [self.k1, self.k2, self.k3]

        # --- Konfiguracja Zbiorników ---
        self.z1 = Zbiornik(ZBIORNIK1_POSX, ZBIORNIK1_POSY, nazwa="Zbiornik")
        self.z1.dodaj_ciecz(50)
        self.z1.aktualizuj_poziom()

        self.zbiorniki = [self.z1]

        # --- Konfiguracja Rur ---
        p_start = self.z1.punkt_gora_srodek()
        p_koniec = self.k1.punkt_wlotu()
        self.r1 = Rura([p_start, (p_start[0], p_start[1]-15), (p_koniec[0]-15,p_start[1]-15), 
                        (p_koniec[0]-15, p_koniec[1]), p_koniec])
        
        p_koniec = self.k2.punkt_wlotu()
        self.r2 = Rura([p_start, (p_start[0], p_start[1]-15), (p_koniec[0]-15,p_start[1]-15), 
                        (p_koniec[0]-15, p_koniec[1]), p_koniec])
        
        p_koniec = self.k3.punkt_wlotu()
        self.r3 = Rura([p_start, (p_start[0], p_start[1]-15), (p_koniec[0]-15,p_start[1]-15), 
                        (p_koniec[0]-15, p_koniec[1]), p_koniec])
        
        p_start = 0, ZBIORNIK1_POSY+15
        p_koniec = ZBIORNIK1_POSX, ZBIORNIK1_POSY+15
        self.r4 = Rura([p_start, p_koniec])
    
        self.rury = [self.r1, self.r2, self.r3, self.r4] 
        
        # --- Konfiguracja Kol ---
        self.kolo1 = Kolo(int(KOMORA1_POSX+self.k1.width/2), int(self.k1.y+200), nazwa="Kolo 1")
        self.kolo2 = Kolo(int(KOMORA2_POSX+self.k2.width/2), int(self.k2.y+200), nazwa="Kolo 2")
        self.kolo3 = Kolo(int(KOMORA3_POSX+self.k3.width/2), int(self.k3.y+200), nazwa="Kolo 3")

        self.kola = [self.kolo1, self.kolo2, self.kolo3]

        # --- Konifugracja Korbowod ---
        self.korbowod1_1 = Korbowod(self.k1.punkt_srodek_tloka, self.kolo1.punkt_zaczepienia) # tlok1 -> kolo1
        self.korbowod1_2 = KorbowodPrzymocowany(int(KOMORA1_POSX+200), int(KOMORA1_POSY+43)) # srodek korbowodu
        self.korbowod1_3 = Korbowod(self.kolo1.punkt_zaczepienia, self.korbowod1_2.punkt_koniec) # kolo1 -> srodek korbowodu
        self.korbowod1_4 = Korbowod(self.korbowod1_2.punkt_start, self.k1.punkt_polaczenie_korbowod) # srodek korbowodu -> tlok2

        self.korbowod2_1 = Korbowod(self.k2.punkt_srodek_tloka, self.kolo2.punkt_zaczepienia) # tlok2 -> kolo2
        self.korbowod2_2 = KorbowodPrzymocowany(int(KOMORA2_POSX+200), int(KOMORA1_POSY+43)) # srodek korbowodu
        self.korbowod2_3 = Korbowod(self.kolo2.punkt_zaczepienia, self.korbowod2_2.punkt_koniec) # kolo2 -> srodek korbowodu
        self.korbowod2_4 = Korbowod(self.korbowod2_2.punkt_start, self.k2.punkt_polaczenie_korbowod) # srodek korbowodu -> tlok2

        self.korbowod3_1 = Korbowod(self.k3.punkt_srodek_tloka, self.kolo3.punkt_zaczepienia) # tlok3 -> kolo3
        self.korbowod3_2 = KorbowodPrzymocowany(int(KOMORA3_POSX+200), int(KOMORA1_POSY+43)) # srodek korbowodu
        self.korbowod3_3 = Korbowod(self.kolo3.punkt_zaczepienia, self.korbowod3_2.punkt_koniec) # kolo3 -> srodek korbowodu
        self.korbowod3_4 = Korbowod(self.korbowod3_2.punkt_start, self.k3.punkt_polaczenie_korbowod) # srodek korbowodu -> tlok3
        
        self.korbowod = [self.korbowod1_1, self.korbowod1_2, self.korbowod1_3, self.korbowod1_4, 
                         self.korbowod2_1, self.korbowod2_2, self.korbowod2_3, self.korbowod2_4,
                         self.korbowod3_1, self.korbowod3_2, self.korbowod3_3, self.korbowod3_4]

        # --- Przyciski ---
        btn_height = 50
        btn_width = 100
        margin = 30
        self.btn1 = QPushButton("START", self)
        self.btn1.setGeometry(margin, HEIGHT-btn_height-margin, btn_width, btn_height)
        self.btn1.setStyleSheet("background-color: yellow; color: black; font-size: 14px")
        self.btn1.clicked.connect(self.przelacz_symulacje)

        btn_width = 125
        self.btn2 = QPushButton("Dodaj 30% pary", self)
        self.btn2.setGeometry(int(KOMORA1_POSX+self.k1.width/2-btn_width/2), HEIGHT-btn_height-margin, btn_width, btn_height)
        self.btn2.setStyleSheet("background-color: green; color: black; font-size: 14px")
        self.btn2.clicked.connect(lambda: self.k1.dodaj_pare(30))
        
        self.btn3 = QPushButton("Dodaj 30% pary", self)
        self.btn3.setGeometry(int(KOMORA2_POSX+self.k2.width/2-btn_width/2), HEIGHT-btn_height-margin, btn_width, btn_height)
        self.btn3.setStyleSheet("background-color: green; color: black; font-size: 14px")
        self.btn3.clicked.connect(lambda: self.k2.dodaj_pare(30))

        self.btn4 = QPushButton("Dodaj 30% pary", self)
        self.btn4.setGeometry(int(KOMORA3_POSX+self.k3.width/2-btn_width/2), HEIGHT-btn_height-margin, btn_width, btn_height)
        self.btn4.setStyleSheet("background-color: green; color: black; font-size: 14px")
        self.btn4.clicked.connect(lambda: self.k3.dodaj_pare(30))

        # --- Suwaki ---
        self.suwak1 = QSlider(Qt.Horizontal, self)
        self.suwak1.setGeometry(int(KOCIOL_POSX), int(KOCIOL_POSY)+200, 100, 20)
        self.suwak1.setMinimum(0)
        self.suwak1.setMaximum(500)
        self.suwak1.valueChanged.connect(self.kociol.ustaw_temp)

        self.suwak2 = QSlider(Qt.Horizontal, self)
        self.suwak2.setGeometry(int(margin+btn_width), int(HEIGHT-margin-btn_height/2), 100, 20)
        self.suwak2.setMinimum(0)
        self.suwak2.setMaximum(100)
        self.suwak2.valueChanged.connect(self.doplyw_wody)
        self.doplyw = 0
        podpis = QLabel("Dopływ wody", self)
        podpis.move(int(margin+btn_width), int(HEIGHT-margin-btn_height/2 -20))
        font = QFont("Arial", 10, QFont.Bold)
        podpis.setStyleSheet("color: white;")
        podpis.setFont(font)

        # --- Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)
        self.running = False
        self.flow_speed = 5*PREDKOSC_SYMULACJI

        self.faza_doplywu1 = True
        self.faza_doplywu2 = True
        self.faza_doplywu3 = True

    def doplyw_wody(self,doplyw):
        max_doplyw = 0.1
        self.doplyw = (doplyw/100)*max_doplyw

    def przelacz_symulacje(self):
        if self.running:
            self.timer.stop()
            self.btn1.setText("START")
        else:
            self.timer.start(20)
            self.btn1.setText("STOP")
        self.running = not self.running

    def logika_przeplywu(self):
        #doplyw wody do zbiornika
        if self.doplyw > 0:
            self.r4.ustaw_przeplyw(True)
            self.z1.dodaj_ciecz(self.doplyw)
        if self.doplyw == 0:
            self.r4.ustaw_przeplyw(False)
        
        #kociol -> Z1 TEMP
        if self.kociol.temperatura > self.z1.temperatura:
            przyrost = ((self.kociol.temperatura - self.z1.temperatura)/500)*PREDKOSC_SYMULACJI
            self.z1.dodaj_temp(przyrost)

        #Z1 -> TEMP SPADEK
        if self.z1.temperatura > 0 and self.z1.temperatura > self.kociol.temperatura:
            spadek = ((self.z1.temperatura-self.kociol.temperatura)/300)*PREDKOSC_SYMULACJI
            self.z1.usun_temp(spadek)

        #Z1 -> WODA -> PARA -> WODA
        mnoznik = 1.004**abs(self.z1.temperatura-100)*3
        self.zapas = 0
        if self.z1.temperatura >= 100:
            usunieto = self.z1.usun_ciecz(0.001*mnoznik)
            if usunieto != 0:
                dodano = self.z1.dodaj_pare(1600*usunieto)
                if dodano != 1600*usunieto:
                    self.zapas = abs(usunieto*1600 - dodano)
        if self.z1.temperatura < 100:
            usunieto = self.z1.usun_pare(1.6*mnoznik)
            if usunieto != 0:
                self.z1.dodaj_ciecz(usunieto/1600)   

        # Z1 -> K1 + obrot kola
        plynie_1 = 0
        plynie_2 = 0
        plynie_3 = 0
        pressure_modifier = 1.004**abs(self.z1.temperatura-100)
        czy1 = not self.k1.czy_pelny() and self.faza_doplywu1
        czy2 = not self.k2.czy_pelny() and self.faza_doplywu2
        czy3 = not self.k3.czy_pelny() and self.faza_doplywu3
        dzielnik = 0
        if czy1: dzielnik += 1
        if czy2: dzielnik += 1
        if czy3: dzielnik += 1
        if czy1 or czy2 or czy3:
            ilosc = self.z1.usun_pare(self.flow_speed*pressure_modifier) + self.zapas
            if ilosc > 0:
                if czy1: 
                    self.k1.dodaj_pare(ilosc/dzielnik)
                    plynie_1 = 2
                if czy2: 
                    self.k2.dodaj_pare(ilosc/dzielnik)
                    plynie_2 = 2
                if czy3: 
                    self.k3.dodaj_pare(ilosc/dzielnik)
                    plynie_3 = 2
                self.kolo1.ustaw_kat(-self.k1.poziom_roboczy*180)
                self.kolo2.ustaw_kat(-self.k2.poziom_roboczy*180)
                self.kolo3.ustaw_kat(-self.k3.poziom_roboczy*180)
        if self.k1.czy_pelny():
            self.faza_doplywu1 = False
            plynie_1 = 0
        if self.k2.czy_pelny():
            self.faza_doplywu2 = False
            plynie_2 = 0
        if self.k3.czy_pelny():
            self.faza_doplywu3 = False
            plynie_3 = 0
        if self.faza_doplywu1 == False:
            ilosc = self.k1.usun_pare(self.flow_speed*pressure_modifier)
            self.kolo1.ustaw_kat(self.k1.poziom_roboczy*180)
            if self.k1.czy_pusty():
                self.faza_doplywu1 = True
        if self.faza_doplywu2 == False:
            ilosc = self.k2.usun_pare(self.flow_speed*pressure_modifier)
            self.kolo2.ustaw_kat(self.k2.poziom_roboczy*180)
            if self.k2.czy_pusty():
                self.faza_doplywu2 = True
        if self.faza_doplywu3 == False:
            ilosc = self.k3.usun_pare(self.flow_speed*pressure_modifier)
            self.kolo3.ustaw_kat(self.k3.poziom_roboczy*180)
            if self.k3.czy_pusty():
                self.faza_doplywu3 = True
        self.r1.ustaw_przeplyw(plynie_1)
        self.r2.ustaw_przeplyw(plynie_2)
        self.r3.ustaw_przeplyw(plynie_3)

        #Kolo1 -> korbowod przymocowany1
        full_kat = 60
        if self.kolo1.kat <= 60 and self.kolo1.kat > -120:
            norm = abs(self.kolo1.kat - 60)/180 #zakres 0-1
            kat = norm*full_kat - full_kat/2
        else:
            if self.kolo1.kat < 0:
                norm = abs(self.kolo1.kat + 120)/180
            else:
                norm = abs(60+(180-self.kolo1.kat))/180
            kat = -norm*full_kat + full_kat/2
        self.korbowod1_2.ustaw_kat(kat)
        #korbowod przymocowany1 -> tlok wpuszczajacy/wypuszczajacy pare1
        if not (self.kolo1.kat <= 60 and self.kolo1.kat > -120):
            norm = 1-norm
        self.k1.ustaw_tlok_blok(norm)

        #Kolo2 -> korbowod przymocowany2
        full_kat = 60
        if self.kolo2.kat <= 60 and self.kolo2.kat > -120:
            norm = abs(self.kolo2.kat - 60)/180 #zakres 0-1
            kat = norm*full_kat - full_kat/2
        else:
            if self.kolo2.kat < 0:
                norm = abs(self.kolo2.kat + 120)/180
            else:
                norm = abs(60+(180-self.kolo2.kat))/180
            kat = -norm*full_kat + full_kat/2
        self.korbowod2_2.ustaw_kat(kat)
        #korbowod przymocowany2 -> tlok wpuszczajacy/wypuszczajacy pare2
        if not (self.kolo2.kat <= 60 and self.kolo2.kat > -120):
            norm = 1-norm
        self.k2.ustaw_tlok_blok(norm)

        #Kolo3 -> korbowod przymocowany3
        full_kat = 60
        if self.kolo3.kat <= 60 and self.kolo3.kat > -120:
            norm = abs(self.kolo3.kat - 60)/180 #zakres 0-1
            kat = norm*full_kat - full_kat/2
        else:
            if self.kolo3.kat < 0:
                norm = abs(self.kolo3.kat + 120)/180
            else:
                norm = abs(60+(180-self.kolo3.kat))/180
            kat = -norm*full_kat + full_kat/2
        self.korbowod3_2.ustaw_kat(kat)
        #korbowod przymocowany3 -> tlok wpuszczajacy/wypuszczajacy pare3
        if not (self.kolo3.kat <= 60 and self.kolo3.kat > -120):
            norm = 1-norm
        self.k3.ustaw_tlok_blok(norm)

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # 1. Rysowanie elementów symulacji
        for r in self.rury:
            r.draw(p)
        for r in self.rury:
            r.draw_przeplyw(p)
        for z in self.zbiorniki:
            z.draw(p)
        for k in self.kola:
            k.draw(p)
        for k in self.komory:
            k.draw(p)
        self.kociol.draw(p)
        for k in self.korbowod:
            k.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec())