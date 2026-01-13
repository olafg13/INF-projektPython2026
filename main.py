import sys
from rura import Rura
from zbiornik import Zbiornik
from kociol import Kociol
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
WIDTH = 900
HEIGHT = 600
KOCIOL_POSX = WIDTH/2
KOCIOL_POSY = 140+(HEIGHT/3)
ZBIORNIK_POSX = WIDTH/2
ZBIORNIK_POSY = HEIGHT/3

# --- GŁÓWNA KLASA SYMULACJI ---
class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zbiorniki")
        self.setFixedSize(WIDTH, HEIGHT)
        self.setStyleSheet("background-color: #2b2b2b;")

        # --- Konfiguracja kotła ---

        self.k1 = Kociol(KOCIOL_POSX, KOCIOL_POSY, nazwa="Kocioł")

        # --- Konfiguracja Zbiorników ---
        self.z1 = Zbiornik(ZBIORNIK_POSX, ZBIORNIK_POSY, nazwa="Zbiornik 1")
        self.z1.aktualna_ilosc = 100.0 
        self.z1.aktualizuj_poziom()

        self.zbiorniki = [self.z1]

        # --- Konfiguracja Rur ---
        p_start = self.z1.punkt_gora_srodek()
        p_koniec = (100,100)
        mid_y = (p_start[1] + p_koniec[1]) / 2
        
        self.rura1 = Rura([p_start, (p_start[0], mid_y), (p_koniec[0], mid_y), p_koniec])
        """
        p_start2 = self.z2.punkt_dol_srodek()
        p_koniec2 = self.z3.punkt_gora_srodek()
        mid_y2 = (p_start2[1] + p_koniec2[1]) / 2

        self.rura2 = Rura([p_start2, (p_start2[0], mid_y2), (p_koniec2[0], mid_y2), p_koniec2])"""
        self.rury = [] 

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
        self.suwak.valueChanged.connect(self.k1.ustaw_temp)

        # --- Timer ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)
        self.running = False
        self.flow_speed = 0.8

    def przelacz_symulacje(self):
        if self.running:
            self.timer.stop()
            self.btn.setText("START")
        else:
            self.timer.start(20)
            self.btn.setText("STOP")
        self.running = not self.running

    def logika_przeplywu(self):
        #K1 -> Z1
        if self.k1.temperatura > self.z1.temperatura:
            przyrost = (self.k1.temperatura - self.z1.temperatura)/500
            self.z1.dodaj_temp(przyrost)
        self.update()

        """# Z1 -> Z2
        plynie_1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            ilosc = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(ilosc)
            plynie_1 = True
        self.rura1.ustaw_przeplyw(plynie_1)

        # Z2 -> Z3
        plynie_2 = False
        if self.z2.aktualna_ilosc > 5.0 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(self.flow_speed)
            self.z3.dodaj_ciecz(ilosc)
            plynie_2 = True
        self.rura2.ustaw_przeplyw(plynie_2)

        self.update() """

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # 1. Rysowanie elementów symulacji
        for r in self.rury:
            r.draw(p)
        for z in self.zbiorniki:
            z.draw(p)
        self.k1.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec())