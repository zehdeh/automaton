#! /usr/local/bin/python3

import sys
import math
import numpy as np
from random import seed,random
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,QtWidgets

class Grid(QtWidgets.QFrame):
	def __init__(self, rows, columns):
		super(Grid, self).__init__()

		self.rows = rows
		self.columns = columns
		self.cellSize = 9
	def paintEvent(self, e):
		painter = QtGui.QPainter(self)

		totalGridHeight = (self.columns*self.cellSize + self.columns+1)
		totalGridWidth = (self.rows*self.cellSize + self.rows+1)
		for i in range(self.columns+1):
			painter.drawLine(\
			self.width()/2 - totalGridWidth/2 + i*self.cellSize + i,\
			self.height()/2 - totalGridHeight/2,\
			self.width()/2 - totalGridWidth/2 + i*self.cellSize + i,\
			self.height()/2 + totalGridHeight/2)

		for i in range(self.rows+1):
			painter.drawLine(\
			self.width()/2 - totalGridWidth/2,\
			self.height()/2 - totalGridHeight/2 + i*self.cellSize+i,\
			self.width()/2 + totalGridWidth/2,\
			self.height()/2 - totalGridHeight/2 + i*self.cellSize+i)

		painter.end()

class Graph:
	def __init__(self, nodeCount):
		self.nodeCount = nodeCount
		self.nodeActivity = np.zeros(nodeCount)
		
		self.edges = set()
		seed()
		for i in range(nodeCount):
			for j in range(nodeCount):
				if i < j and random() < 0.01:
					self.edges.add((i,j))


class GraphView(QtWidgets.QFrame):
	def __init__(self, graph):
		super(GraphView, self).__init__()

		self.graph = graph
		self.columns = int(math.sqrt(self.graph.nodeCount))
		self.rows = int(math.sqrt(self.graph.nodeCount))
		self.nodeRadius = 4
		self.margin = 30

		self.totalGraphWidth = self.rows*(2*self.nodeRadius + self.margin)
		self.totalGraphHeight = self.columns*(2*self.nodeRadius + self.margin)
	def paintEdge(self, painter, i, j):

		painter.drawLine((self.width() - self.totalGraphWidth)/2 + (i % self.columns)*(2*self.nodeRadius + self.margin) + self.nodeRadius,\
		(self.height() - self.totalGraphHeight)/2 + int(i / self.columns)*(2*self.nodeRadius + self.margin) + self.nodeRadius,\
		(self.width() - self.totalGraphWidth)/2 + (j % self.columns)*(2*self.nodeRadius + self.margin) + self.nodeRadius,\
		(self.height() - self.totalGraphHeight)/2 + int(j / self.columns)*(2*self.nodeRadius + self.margin) + self.nodeRadius)

	def paintEvent(self, e):
		painter = QtGui.QPainter(self)

		painter.setPen(Qt.darkGray)
		for edge in self.graph.edges:
			self.paintEdge(painter, edge[0], edge[1])

		painter.setPen(Qt.black)
		painter.setBrush(Qt.white)
		for i in range(self.columns):
			for j in range(self.rows):
				painter.setBrush(Qt.red if self.graph.nodeActivity[i*self.columns + j] == 1 else Qt.white)
				painter.drawEllipse((self.width() - self.totalGraphWidth)/2 + i*(2*self.nodeRadius + self.margin), (self.height() - self.totalGraphHeight)/2 + j*(2*self.nodeRadius + self.margin), 2*self.nodeRadius, 2*self.nodeRadius)

		painter.end()

class Window(QtWidgets.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()

		self.statusBar().showMessage("Ready")
		self.setFixedSize(800,800)
		self.show()

		self.splitter = QtWidgets.QSplitter(Qt.Vertical)

		self.graph = Graph(20*20)
		self.graph.nodeActivity[int(self.graph.nodeCount / 2)] = 1
		self.graph.nodeActivity[int(self.graph.nodeCount / 2)+1] = 1

		self.graphView = GraphView(self.graph)
		#self.splitter.addWidget(self.grid)
		#self.splitter.addWidget(self.graph)

		self.setCentralWidget(self.graphView)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())
