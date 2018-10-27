from math import sqrt



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


def getAreaCenter(a, b):

	dx, dy = abs(a.x() - b.x()), abs(a.y() - b.y())
	return QPoint(a.x() + dx // 2 if a.x() < b.x() else b.x() + dx // 2, a.y() + dy // 2 if a.y() < b.y() else b.y() + dy // 2)


def BresenhamLine(leftP, rightP):
 
	deltaErr = abs(float(leftP.y() - rightP.y()) / float(leftP.x() - rightP.x()))
	leftP, rightP = (leftP, rightP) if leftP.x() < rightP.x() else (rightP, leftP)
	yield QPoint(leftP.x(), rightP.x())
	err, yinc, y = deltaErr, 1 if leftP.y() < rightP.y() else -1, min(leftP.y(), rightP.y())
	for x in range(leftP.x() + 1, rightP.x() + 1):
		if err > 0.5:
			err -= 1.0
			y += yinc
		err += deltaErr
		yield QPoint(x, y) 




