import sys
from random import randint
from functools import reduce

from geometry import *
from structures import *

from math import pi

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QPointF, QTimer
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
		self.dx = 0
		self.dy = 0
		self.mousePrevPos = QPoint()
		self.keyHandler('adfdsf')

	def resizeEvent(self, event):
		self.buffImage = QPixmap(self.width(), self.height())
		self._fill()

	def keyHandler(self, key):
		if key == Qt.Key_Enter or True:

			center = getAreaCenter(QPoint(0, 0), QPoint(self.width(), self.height()))

			a = Point(float(center.x() + 100), center.y(), -100)
			b = Point(center.x() -100, center.y(), -150)
			c = Point(center.x(), center.y() - 73, -50)
			d = Point(center.x(), center.y() + 50, -0)

			self.shapes.append(Tetrahedron(a,b,c,d))

			self.shapes[-1].setBorderColor(QColor(129,0,38))

	def _paint(self, event, f):
		f(event)

	def paintFuncs(self):
		self.onPaint()

	def deltaToUngle(self, pos):
		normalCoef = 1
		self.dx = (pos.x() - self.mousePrevPos.x())/ normalCoef * pi / 180.0
		self.dy = (pos.x() - self.mousePrevPos.x())/normalCoef * pi / 180.0

		self.dy, self.dx = self.dx, self.dy
		self._fill()
		self.repaint()
		self.dx = 0
		self.dy = 0

	def drawShape(self, shape):
		self.painter.setPen(shape.getBorderColor())
		for j in drawEdges(shape):
			self.painter.drawPoint(j)
		self.painter.setPen(shape.getCenterColor())
		for i in drawPoint(shape.getCenter()):
			print('----', i)
			self.painter.drawPoint(i)


	def _fill(self):
		self.buffImage = QPixmap(self.width(), self.height())
		self.painter = QPainter()
		self.painter.begin(self.buffImage) 
		self.painter.setPen(QColor(129,0,38))
		for shape in self.shapes:
			shape.turnAroundX(self.dx)
			#shape.turnAroundY(self.dy)
			self.drawShape(shape)
			'''
			for j in drawEdges(shape):
				self.painter.drawPoint(j)
			'''
		self.painter.end()


	def __fill(self):
		self.painter = QPainter()
		self.painter.begin(self.buffImage)
		#self.painter.drawPixmap(buffImage)
		
		self.painter.setPen(QColor(129,0,38))


		triangle = Triangle(a,b,c)
		area = getArea(triangle.getVertices())

		for i in fillTriangle(area, triangle):
			self.painter.drawPoint(i)

		self.painter.setPen(QColor(255,128,0))
		for i in getBorder([Edge(a,b), Edge(b,c), Edge(a,c)]):

			self.painter.drawPoint(i)

		self.painter.end()

	def paintEvent(self, event):
		self.painter = QPainter()
		self.painter.begin(self)
		self.painter.drawPixmap(0,0, self.buffImage)
		self.painter.end()


	def keyPressEvent(self, event):
		pass
		#self.keyHandler(event.key())

	def mousePressEvent(self, event):
		center = getAreaCenter(QPoint(0, 0), QPoint(self.width(), self.height()))
		self.mousePrevPos = event.pos()
		#print(self.shapes)
		'''
		a = QPoint(center.x() + 100, center.y())
		b = QPoint(center.x() -100, center.y())
		c = QPoint(center.x(), center.y() -50)
		self.pressed = True
		'''
		self._fill()
		self.repaint()
		self.pressed = False

	def mouseMoveEvent(self, event):
		self.deltaToUngle(event.pos())
		self.mousePrevPos = event.pos()




app = QApplication(sys.argv)

widget = DrawEngine()
widget.resize(700, 500)
widget.show()

timer = QTimer()

#timer.timeout.connect()

sys.exit(app.exec_())
