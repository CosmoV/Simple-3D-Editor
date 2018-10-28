from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
	QFileDialog, QGridLayout, QPushButton, QMainWindow, QLineEdit, QTextEdit, QTabWidget, QSizePolicy,
	QGraphicsView, QGraphicsItem, QGraphicsScene
	)

from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QTimer, QRectF, QRect

from geometry import * 
from math import cos, sin


class Matrix():

	def __init__(self, rows = None):
		self.rows = rows if rows else []

	def addRow(self, row):
		self.rows.append(row)

	def rows(self):
		return self.rows

	def __mul__(self, other):
		res = [[0 for _ in range(len(rows[0]))] for _ in range(len(rows))]
		for i in range(len(rows)):
			for j in range(len(rows[0])):
				res[i][j] = sum(self.rows[i][k] * other.rows[k][i] for k in range(len(rows[0])))
		return Matrix(res)



class Vector():

	def __init__(self, first, second):
		self.first = first
		self.second = second

	def __add__(self, other):
		#print('-------\n', self,  other, sep = '\n')
		a = Point(*(self.first[i] + other.first[i] for i in range(len(self.first))))
		b = Point(*(self.second[i] + other.second[i] for i in range(len(self.second))))
		#print( a, b)
		return Vector(a, b)

	def __sub__(self, other):
		a = Point(*(self.first[i] - other.first[i] for i in range(len(self.first))))
		b = Point(*(self.second[i] - other.second[i] for i in range(len(self.second))))
		return Vector(a, b)

	def __mul__(self, value):
		a = Point(*(self.first[i] * value for i in range(len(self.first))))
		b = Point(*(self.second[i] * value for i in range(len(self.second))))
		return Vector(a, b)

	def __truediv__(self, value):
		a = Point(*(self.first[i] * value for i in range(len(self.first))))
		b = Point(*(self.second[i] * value for i in range(len(self.second))))
		return Vector(a, b)

	def __str__(self):
		return 'A: {0}, B: {1}'.format(self.first, self.second)

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

	def __str__(self):
		return 'A: {0}, B: {1}'.format(self.first, self.second)


class Point():

	def __init__(self, *values):
		self.values = [0 for i in range(max(len(values), 3))]
		for i in range(len(values)):
			self.values[i] = values[i]

	def x(self):
		return self.values[0]

	def y(self):
		return self.values[1]

	def z(self):
		return self.values[2]


	def dist(self, other):
		return dist(self, other)

	def __getitem__(self, key):
		return self.values[key]

	def __setitem__(self, key, value):
		self.values[key] = value

	def __len__(self):
		return len(self.values)

	def __add__(self, other):
		return Point(*(self[i] + other[i] for i in range(len(other))))

	def __truediv__(self, value):
		return Point(*(i / value  for i in self.values))

	def __str__(self):
		return 'X: {0}, Y: {1}, Z: {2}'.format(self[0], self[1], self[2])


class Face():


	def Square(self):
		pass



class Shape():

	def __init__(self):
		self.setBorderColor()
		self.setCenterColor()
	def getEdges(self):
		pass

	def getVertices(self):
		pass

	def setVertices(self, *vertices):
		self.vertices = [i for i in vertices]
	
	def getFaces(self):
		pass

	def volume(self):
		pass

	def setBorderColor(self, color = QColor(0, 0, 0)):
		self.borderColor = color

	def getBorderColor(self):
		return self.borderColor

	def setCenterColor(self, color = QColor(255, 255, 0)):
		self.setCenterPointColor = color

	def getCenterColor(self):
		return self.setCenterPointColor

	def getCenter(self):
		O, vertices = Point(), self.getVertices()
		#print('center', vertices)
		st = Vector(O, O)
		for i in vertices:
			st = st +  Vector(O, i)
		print('center', st / len(vertices))
		return st / len(vertices)

	def getCenterDiff(self):
		O, center = Point(), self.getCenter() 
		print('------------------------')
		for i in [Vector(O, i) - center for i in self.getVertices()]:
			print(i)
		print('/////////////////////')
		return [Vector(O, i) - center for i in self.getVertices()]

	def turnAround(self, alpha = 0, beta = 0, gamma = 0):
		O, center = Point(), self.getCenter()

		for i in (i.second for i in self.getCenterDiff()):
			print(i)
		self.setVertices(*(i.second for i in self.getCenterDiff()))

		if alpha:
			self.turnAroundX(alpha)
		if beta:
			self.turnAroundY(beta)
		if gamma:
			self.turnAroundZ(gamma)

		self.setVertices(*(i.second for i in (Vector(O, v) + center for v in self.getVertices())))




	def _turnAroundY(self, p, alpha):
		return Point(p.x() * cos(alpha) - p.z() * sin(alpha), p.y(), - p.x() * sin(alpha) + p.z() * cos(alpha))  

	def turnAroundY(self, alpha):
		self.vertices = [self._turnAroundY(v, alpha) for v in self.vertices]
		self.createEdges()

	def _turnAroundX(self, p, alpha):
		return Point(p.x(), p.y() * cos(alpha) + p.z() * sin(alpha), - p.y() * sin(alpha) + p.z() * cos(alpha))  

	def turnAroundX(self, alpha):
		self.vertices = [self._turnAroundX(v, alpha) for v in self.vertices]
		self.createEdges()

	def _turnAroundZ(self, p, alpha):
		return Point(p.x() * cos(alpha) - p.y() * sin(alpha), p.x() * sin(alpha) + p.y() * cos(alpha), p.z())  

	def turnAroundZ(self, alpha):
		self.vertices = [self._turnAroundZ(v, alpha) for v in self.vertices]
		self.createEdges()




class Triangle(Shape, QGraphicsItem):

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



class Tetrahedron(Shape):

	def __init__(self, a, b, c, d):
		super().__init__()
		self.vertices = [a,b,c,d]
		self.createEdges()

	def setVertices(self, *vertices):
		self.vertices = [i for i in vertices]
		self.createEdges()

	def createEdges(self):
		self.edges = []
		for i in range(len(self.vertices)):
			for j in range(i+1, len(self.vertices)):
				self.edges.append(Edge(self.vertices[i], self.vertices[j]))

	def getVertices(self):
		return self.vertices

	def getCenter(self):
		_sum = Point()
		for i in self.vertices:
			_sum += i
		return _sum / 4


	def getEdges(self):
		return self.edges




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





