import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont

# --- KLASA KOŁO ---
class Kolo:
    def __init__(self, x, y, r = 150, nazwa=""):
        self.x = x
        self.y = y
        self.r = r
        self.nazwa = nazwa
        self.kat = 0
    
    def dodaj_kat(self, ilosc):
        self.kat += ilosc

    def usun_kat(self, ilosc):
        self.kat -= ilosc

    def ustaw_kat(self, ilosc):
        self.kat = ilosc

    def punkt_zaczepienia(self):
        angle = (2*math.pi/360)*(self.kat-90)
        p_x = int(self.x + 56*math.cos(angle))
        p_y = int(self.y + 56*math.sin(angle))
        return (p_x, p_y)

    def draw(self, painter):
        painter.save()
        pen = QPen(Qt.white, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        #Koło
        painter.drawEllipse(self.x - self.r, self.y - self.r, 2*self.r, 2*self.r)
        painter.translate(self.x,self.y)
        painter.rotate(self.kat)
        #Szprychy
        for i in range(3):
            s_angle = i*(2*math.pi)/3
            s_x = self.r*math.cos(s_angle)
            s_y = self.r*math.sin(s_angle)
            painter.drawLine(int(-s_x), int(-s_y), int(s_x), int(s_y))
        #Obciazenie
        pen = QPen(Qt.black, 3)
        painter.setBrush(QColor(255, 255, 255)) 
        painter.setPen(pen)
        painter.drawRect(-15, -80, 30, 100)  
        painter.drawEllipse(-50, 15, 100, 60)
        painter.restore()