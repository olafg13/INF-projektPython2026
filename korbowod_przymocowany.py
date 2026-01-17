import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont

# --- KLASA KORBOWOD_PRZYMOCOWANY ---

class KorbowodPrzymocowany:
    def __init__(self, x, y, grubosc=8):
        self.x = x
        self.y = y
        self.start = x, y-30
        self.koniec = x, y+120
        self.grubosc = grubosc
        self.kat = 0
    
    def punkt_start(self):
        start = int(self.x+30*math.sin(math.radians(self.kat))), int(self.y-30*math.cos(math.radians(self.kat)))
        return start
    
    def punkt_koniec(self):
        koniec = int(self.x-120*math.sin(math.radians(self.kat))), int(self.y+120*math.cos(math.radians(self.kat)))
        return koniec
    
    def ustaw_kat(self, kat):
        self.kat = kat
    
    def draw(self, painter):
        painter.save()
        pen = QPen(Qt.gray, 8)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.translate(self.x, self.y)
        painter.rotate(self.kat)
        painter.translate(-self.x, -self.y)
        start = self.start
        koniec = self.koniec
        painter.drawLine(int(start[0]),int(start[1]), int(koniec[0]), int(koniec[1]))
        painter.setBrush(Qt.black)
        x, y = start
        r = 10
        painter.drawEllipse(int(self.x-r), int(self.y-r), int(2*r), int(2*r))
        painter.drawEllipse(int(x-10), int(y-10), int(2*r), int(2*r))
        x,y = koniec
        painter.drawEllipse(int(x-10), int(y-10), int(2*r), int(2*r))
        painter.restore()