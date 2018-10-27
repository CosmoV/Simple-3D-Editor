from geometry import *


class GObject():
	
	def __init__(self):
		self.vertices = []

	def setVertices(self, vertices):
		for i in vertices:
			print(i)
			self.vertices.append(i)


class Downloader():
	
	def parseVertices(self, s):
		return [GPoint(float(e[1]), float(e[2]), float(e[3])) for e in s if e[0] == 'v']

	def read(self, filename):

		s = [i.split(' ') for i in open(filename).read().split('\n')]

		obj = GObject()
		obj.setVertices(self.parseVertices(s))

downloader = Downloader()

downloader.read('obj.obj')