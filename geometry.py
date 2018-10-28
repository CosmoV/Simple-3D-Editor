from math import sqrt
from collections import namedtuple

from PyQt5.QtCore import QPoint, QPointF

from structures import *
from functools import reduce



def getAreaCenter(a, b):
	dx, dy = abs(a.x() - b.x()), abs(a.y() - b.y())
	return QPoint(a.x() + dx // 2 if a.x() < b.x() else b.x() + dx // 2, a.y() + dy // 2 if a.y() < b.y() else b.y() + dy // 2)

def dist(a,b):
	return sqrt((a.x() - b.x())**2 + (a.y() - b.y())**2 + (a.z() - b.z())**2)  

def drawPoint(p):
	counter = 0
	for i in range(int(p.x()) - 2, int(p.x() + 3)):
		for j in range(int(p.y()) - 1, int(p.y() + 2)):
				yield QPoint(i, j)	
	for i in range(int(p.x()) - 1, int(p.x()) + 1):
		yield QPoint(i, int(p.y()) - 2)
		yield QPoint(i, int(p.y()) + 2)
	
def BresenhamLine(leftP, rightP):
	if leftP.x() != rightP.x():
		deltaErr = abs(float(leftP.y() - rightP.y()) / float(leftP.x() - rightP.x()))
		if deltaErr < 1:
			leftP, rightP = (leftP, rightP) if leftP.x() < rightP.x() else (rightP, leftP)
			yield QPointF(leftP.x(), leftP.y())
			err, yinc, y = 0.0, 1.0 if leftP.y() < rightP.y() else -1.0, leftP.y()
			for x in range(int(leftP.x()) + 1, int(rightP.x()) + 1):
				err += deltaErr
				if err >= 0.5:
					err -= 1.0
					y += yinc
				yield QPoint(x, y)
		else:
			for i in BresenhamLine(Point(leftP.y(), leftP.x()), Point(rightP.y(), rightP.x())):
				yield QPoint(i.y(), i.x())
	else: 
		a = int(min(leftP.y(), rightP.y()))
		for i in range(1 if not a else a, int(max(leftP.y(), rightP.y()) + 1)):
			yield QPointF(leftP.x(), i) 


def getBorder(edgesList):
	for i in (BresenhamLine(edge.first, edge.second) for edge in edgesList):
		for point in i:
			yield point


def pointIn(triangle, point):
	a, b, c = triangle.getA(), triangle.getB(), triangle.getC()
	f = (a.x() - point.x()) * (b.y() - a.y()) - (b.x() - a.x()) * (a.y() - point.y()) < 0
	s = (b.x() - point.x()) * (c.y() - b.y()) - (c.x() - b.x()) * (b.y() - point.y()) < 0
	t = (c.x() - point.x()) * (a.y() - c.y()) - (a.x() - c.x()) * (c.y() - point.y()) < 0
	return f and s and t if f else not f and not s and not t


def fillTriangle(area, triangle):
	for i in range(area.a.x(), area.b.x() + 1):
		for j in range(area.a.y(), area.b.y() + 1):
			point = QPoint(i, j)
			if pointIn(triangle, point):
				yield point


def getArea(pointsList):
	minx = reduce(lambda a, b: a if a < b.x() else b.x(), pointsList, pointsList[0].x())
	maxx = reduce(lambda a, b: a if a > b.x() else b.x(), pointsList, pointsList[0].x())
	miny = reduce(lambda a, b: a if a < b.y() else b.y(), pointsList, pointsList[0].y())
	maxy = reduce(lambda a, b: a if a > b.y() else b.y(), pointsList, pointsList[0].y())
	return namedtuple('Area', 'a b')(QPoint(minx, miny), QPoint(maxx, maxy))



def drawEdges(shape):
	yield from getBorder(shape.getEdges())


