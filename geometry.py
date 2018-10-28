from math import sqrt
from collections import namedtuple

from PyQt5.QtCore import QPoint

from structures import *
from functools import reduce



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


def getAreaCenter(a, b):

	dx, dy = abs(a.x() - b.x()), abs(a.y() - b.y())
	return QPoint(a.x() + dx // 2 if a.x() < b.x() else b.x() + dx // 2, a.y() + dy // 2 if a.y() < b.y() else b.y() + dy // 2)


def BresenhamLine(leftP, rightP):
	if leftP.x() != rightP.x():
		deltaErr = abs(float(leftP.y() - rightP.y()) / float(leftP.x() - rightP.x()))
		leftP, rightP = (leftP, rightP) if leftP.x() < rightP.x() else (rightP, leftP)
		yield QPoint(leftP.x(), leftP.y())
		err, yinc, y = deltaErr, 1 if leftP.y() < rightP.y() else -1, leftP.y()
		for x in range(int(leftP.x()) + 1, int(rightP.x()) + 1):
			if err > 0.5:
				err -= 1.0
				y += yinc
			err += deltaErr
			yield QPoint(x, y) 
	else: 
		a = int(min(leftP.y(), rightP.y()))
		for i in range(1 if not a else a, int(max(leftP.y(), rightP.y()) + 1)):
			yield QPoint(leftP.x(), i) 


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
	print(len(shape.getEdges()))
	yield from getBorder(shape.getEdges())

