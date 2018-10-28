from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
	QFileDialog, QGridLayout, QPushButton, QMainWindow, QLineEdit, QTextEdit, QTabWidget, QSizePolicy,
	QGraphicsView, QGraphicsItem, QGraphicsScene
	)

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QTimer, QRectF, QRect

from geometry import * 
from math import cos, sin




class Line():

	def __init__(self, a = None, b = None):

		def xor(a, b):
			return bool(a) != bool(b)
		
		if not xor(a,b) and a:
			self.a = a
			self.b = b
		else:
			self.a = QPoint(0,0)
			self.b = self.a

	def setPoints(self, a, b):   
		self.a, self.b = a, b

	@property
	def first(self):
		return self.a

	@first.setter
	def first_set(self, value):
		self.a = value
	
	@property
	def second(self):
		return self.b

	@second.setter
	def second(self, value):
		self.b = value

	def __len__(self):
		return sqrt(float((self.a.x() - self.b.x())**2 + (self.a.y() - self.b.y())**2))


class Edge(Line):
	
	def __init__(self, a, b):

		super().__init__(a, b)

	def __mul__(self, other):
		return self.first*other.first + self.second*other.second


class Point():

	def __init__(self, x,y,z = 0):
		self._x = x
		self._y = y
		self._z = z
		self.screenCoords = QPoint(0,0)

	def x(self):
		return self._x

	def y(self):
		return self._y

	def z(self):
		return self._z


	def __str__(self):
		return 'X: {0}, Y: {1}, Z: {2}'.format(self._x, self._y, self._z)


class PointI():

	def __init__(self, x,y,z = 0.0):
		self._x = x
		self._y = y
		self._z = z
		self.screenCoords = QPoint(0,0)

	def x(self):
		return int(self._x)

	def y(self):
		return (self._y)

	def z(self):
		return (self._z)


	def __str__(self):
		return 'X: {0}, Y: {1}, Z: {2}'.format(self.x, self.y, self.z)

class Face():


	def Square(self):
		pass



class ShapeAbstract():

	def getEdges(self):
		pass

	def getVertices(self):
		pass
	
	def getFaces(self):
		pass

	def Volume(self):
		pass



class Triangle(ShapeAbstract, QGraphicsItem):

	def __init__(self, a,b,c):
		super().__init__()
		self.a = a
		self.b = b
		self.c = c

	def setA(self, a):
		self.a = a

	def setB(self, b):
		self.b = b
	
	def setC(self, c):
		self.c = c

	def getA(self):
		return self.a

	def getB(self):
		return self.b

	def getC(self):
		return self.c

	def getVertices(self):
		return [self.a, self.b, self.c]

	def getEdges(self):
		return [Edge(self.a, self.b), Edge(self.b, self.c), Edge(self.c, self.a)]



class Tetrahedron(ShapeAbstract):

	def __init__(self, a, b, c, d):
		super().__init__()
		self.vertices = [a,b,c,d]
		self.createEdges()

	def createEdges(self):
		self.edges = []
		for i in range(len(self.vertices)):
			for j in range(i+1, len(self.vertices)):
				self.edges.append(Edge(self.vertices[i], self.vertices[j]))

	def getVertices(self):
		return self.vertices

	def getEdges(self):
		return self.edges

	'''
	x'=x*cos(L)+z*sin(L);
	y'=y;
	z'=-x*sin(L)+z*cos(L);
	'''
	def _turnAroundY(self, p, alpha):
		return Point(p.x() * cos(alpha) + p.z() * sin(alpha), p.y(), - p.x() * sin(alpha) + p.z() * cos(alpha))  

	def turnAroundY(self, alpha):
		buff, self.vertices = self.vertices, []
		
		for v in buff:
			self.vertices.append(self._turnAroundY(v, alpha))
			print('{0}\n{1}\n--------------'.format(v, self.vertices[-1]))
		
		self.createEdges()


	'''x'=x;
	y':=y*cos(L)+z*sin(L) ;
	z':=-y*sin(L)+z*cos(L) ;
	'''

	def _turnAroundX(self, p, alpha):
		return Point(p.x(), p.y() * cos(alpha) + p.z() * sin(alpha), - p.y() * sin(alpha) + p.z() * cos(alpha))  

	def turnAroundX(self, alpha):
		buff, self.vertices = self.vertices, []
		
		for v in buff:
			self.vertices.append(self._turnAroundX(v, alpha))
			print('{0}\n{1}\n--------------'.format(v, self.vertices[-1]))
		
		self.createEdges()

















'''
#paint(QPainter * painter, const QStyleOptionGraphicsItem * option, QWidget * widget = 0) = 0
	def contains(self, point):
		return pointIn(self, point) 

	def paint(self, painter, options, parent):
		area = getArea(self.getVertices())

		painter.setPen(QColor(255,128,0))

		for i in fillTriangle(area, self):
			painter.drawPoint(i)

	def boundingRect(self):
		area = getArea(self.getVertices())
		return QRectF(area.a, area.b)
'''





