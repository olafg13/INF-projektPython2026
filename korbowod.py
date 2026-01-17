import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont

# --- KLASA KORBOWOD ---

class Korbowod:
    def __init__(self, start, koniec, grubosc=8):
        self.start = start
        self.koniec = koniec
        self.grubosc = grubosc
    def draw(self, painter):
        pen = QPen(Qt.gray, 8)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        start = self.start()
        koniec = self.koniec()
        painter.drawLine(int(start[0]),int(start[1]), int(koniec[0]), int(koniec[1]))
        painter.setBrush(Qt.black)
        x, y = start
        r = 10
        painter.drawEllipse(x-10, y-10, 2*r, 2*r)
        x,y = koniec
        painter.drawEllipse(x-10, y-10, 2*r, 2*r)