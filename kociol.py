import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont

# --- KLASA KOCIOL ---
class Kociol:
    def __init__(self, x, y, width=100, height=50, nazwa=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.nazwa = nazwa
        self.temperatura = 0
        self.maxTemp = 500

    def ustaw_temp(self, temp):
        self.temperatura = temp
        return temp

    def dodaj_temp(self, ilosc):
        wolne = self.maxTemp - self.temperatura
        dodano = min(ilosc, wolne)
        self.temperatura += dodano
        return dodano

    def usun_temp(self, ilosc):
        usunieto = min(ilosc, self.temperatura)
        self.temperatura -= usunieto
        return usunieto

    def draw(self, painter):

        # 1. Rysowanie ognia
        painter.save()
        skala = self.temperatura/self.maxTemp
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 120, 0))
        painter.translate(self.x+self.width/2,self.y+110)
        painter.scale(math.sqrt(skala),math.sqrt(skala))
        path1 = QPainterPath()
        path1.moveTo(0,0)
        path1.cubicTo(0, 0, -30, -50, 0, -100)
        path1.cubicTo(0, -100, 30, -50, 0, 0)
        path1.closeSubpath()
        painter.drawPath(path1)

        painter.translate(20,25)
        path2 = QPainterPath()
        path2.moveTo(0,0)
        path2.cubicTo(0, 0, -30, -50, 0, -100)
        path2.cubicTo(0, -100, 30, -50, 0, 0)
        path2.closeSubpath()
        painter.drawPath(path2)

        painter.translate(-40,0)
        path3 = QPainterPath()
        path3.moveTo(0,0)
        path3.cubicTo(0, 0, -30, -50, 0, -100)
        path3.cubicTo(0, -100, 30, -50, 0, 0)
        path3.closeSubpath()
        painter.drawPath(path3)

        # 2. Rysowanie kotla
        painter.restore()
        pen = QPen(Qt.white, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.white)
        painter.drawRect(int(self.x), int(self.y+100), int(self.width), int(self.height))

        # 3. Podpis pod kotlem
        painter.setPen(Qt.white)
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)
        painter.drawText(int(self.x), int(self.y+170), self.nazwa)
        painter.drawText(int(self.x), int(self.y+185), str(self.temperatura)+"°C")