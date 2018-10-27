import sys
from random import randint

from geometry import *

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
	QFileDialog, QGridLayout, QPushButton, QMainWindow, QLineEdit, QTextEdit, QTabWidget, QSizePolicy,
	QGraphicsView, QGraphicsItem
	)


class DrawEngine(QWidget):

	def __init__(self):
		super().__init__()
		self.paintEventHandler = lambda event, f: True
		self.image = set()
		self.buffImage = set()


	def _paint(self, event, f):
		f(event)

	def paintFuncs(self):
		self.onPaint()

	def byMousePress(self):
		f = lambda : randint(0, 255) 
		painter = QPainter()
		painter.begin(self) 
		painter.setPen(QColor(0,0,0))

		for i in range(100):
			painter.drawPoint(f(),f())

		painter.end()

	def onPaint(self):
		painter = QPainter()
		painter.begin(self) 
		painter.setPen(QColor(0,0,0))

		for i in range(100):
			painter.drawPoint(50-i,i)

		painter.end()

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self) 
		painter.setPen(QColor(0,0,0))
		center = getAreaCenter(QPoint(0, 0), QPoint(self.width(), self.height()))

		for i in BresenhamLine(QPoint(center.x(), center.y()), QPoint(center.x(), center.y() - 200)):
			painter.drawPoint(i)
			print(i)
		painter.end()
		#self.onPaint()
		#self.byMousePress()


	def mousePressEvent(self, event):
		self.pressed = True
		#self.repaint()
		self.pressed = False

app = QApplication(sys.argv)

widget = DrawEngine()
widget.resize(700, 500)
widget.show()

sys.exit(app.exec_())
