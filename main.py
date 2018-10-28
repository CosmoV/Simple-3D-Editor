import sys
from random import randint
from functools import reduce

from geometry import *
from structures import *

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
	QFileDialog, QGridLayout, QPushButton, QMainWindow, QLineEdit, QTextEdit, QTabWidget, QSizePolicy,
	QGraphicsView, QGraphicsItem, QGraphicsScene
	)





class DrawEngine(QWidget):

	def __init__(self):
		super().__init__()
		self.paintEventHandler = lambda event, f: True
		self.image = set()
		self.buffImage = QPixmap(self.width(), self.height())
		self.shapes = []

	def resizeEvent(self, event):
		self.buffImage = QPixmap(self.width(), self.height())
		self._fill()


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

	def _fill(self):
		self.painter = QPainter()
		self.painter.begin(self.buffImage)
		#self.painter.drawPixmap(buffImage)
		
		self.painter.setPen(QColor(129,0,38))
		center = getAreaCenter(QPoint(0, 0), QPoint(self.width(), self.height()))

		a = QPoint(center.x() + 100, center.y())
		b = QPoint(center.x() -100, center.y())
		c = QPoint(center.x(), center.y() -50)

		triangle = Triangle(a,b,c)
		area = getArea(triangle.getVertices())

		for i in fillTriangle(area, triangle):
			self.painter.drawPoint(i)

		self.painter.setPen(QColor(255,128,0))
		for i in getBorder([Edge(a,b), Edge(b,c), Edge(a,c)]):

			self.painter.drawPoint(i)

		'''
		a, b, c = QPoint(center.x(), center.y()-50), QPoint(center.x()+15, center.y()-70), QPoint(center.x()-100, center.y()+60)
		for i in getBorder([Edge(a,b), Edge(b,c), Edge(c,a)]):
			painter.drawPoint(i)		
		'''
		self.painter.end()

	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(0,0, self.buffImage)
		self.painter.end()
		#self.onPaint()
		#self.byMousePress()


	def mousePressEvent(self, event):
		self.pressed = True
		self._fill()
		self.repaint()
		self.pressed = False




app = QApplication(sys.argv)

widget = DrawEngine()
widget.resize(700, 500)
widget.show()

timer = QTimer()

#timer.timeout.connect()

sys.exit(app.exec_())
