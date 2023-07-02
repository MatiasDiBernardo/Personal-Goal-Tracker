from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GUI_design import Ui_MainWindow
from GUI_design2win import Ui_SecondWindow
from GUI_design3stats import Ui_MainWindowStats
import utils as UT
import sys

#pyuic5 -x file.ui -o file.py
#Command for image changes in the resource file name img2 and imagetest
#pyrcc5 -o resources.py resource/resources.qrc

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.fileData = "D:\\Programas\\Proyectos_py\\PersonalGoalsTracker\\data.xlsx"
		self.allData, self.levels, self.actualState = self.loadData()
		self.initalStateSave = self.actualState.copy()
		UT.setMainWin(self.ui, self.actualState, self.levels)

		self.ui.labelProgramming.mousePressEvent = self.click1
		self.ui.labelReading.mousePressEvent = self.click2
		self.ui.labelMusic.mousePressEvent = self.click3
		self.ui.labelGaming.mousePressEvent = self.click4
		self.ui.labelLanguege.mousePressEvent = self.click5
		self.ui.labelLanguege.setText("Others")
		self.ui.labelWatched.mousePressEvent = self.click6

		self.ui.buttonSave.clicked.connect(self.saveEntries)
		self.ui.buttonStats.clicked.connect(self.winStats)

	def loadData(self):
		"""
		Read from the excel data the current status of data and levels
		"""
		df = pd.read_excel(self.fileData)
		dicc = df.to_dict('list')
		actualState = UT.getHoursFromData(dicc)
		levels = UT.getLevelFromData(actualState)

		return dicc, levels, actualState

	def newWin(self):
		"""
		New window with the menu of the specifit category
		"""
		self.window = QMainWindow()
		self.ui2 = Ui_SecondWindow()
		self.ui2.setupUi(self.window)

		self.ui2.addButtonAct1.clicked.connect(self.addHour1)
		self.ui2.addButtonAct2.clicked.connect(self.addHour2)
		self.ui2.addButtonAct3.clicked.connect(self.addHour3)

		self.ui2.minusButtonAct1.clicked.connect(self.minusHour1)
		self.ui2.minusButtonAct2.clicked.connect(self.minusHour2)
		self.ui2.minusButtonAct3.clicked.connect(self.minusHour3)
		self.window.show()
	
	def winStats(self):
		"""
		Window that displays the statistics and graphs
		"""
		self.winS = QMainWindow()
		self.ui3 = Ui_MainWindowStats() 
		self.ui3.setupUi(self.winS)
		self.winS.show()

		self.ui3.pushButton.clicked.connect(self.plotGraph)  #Graph Button

		self.layoutPlot = QtWidgets.QHBoxLayout(self.ui3.framePlot)
		self.layoutPlot.setObjectName("layoutPlot")

		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.layoutPlot.addWidget(self.canvas)
	
	def plotGraph(self):
		self.figure.clear()
		typePlot = self.ui3.typeBox.currentText()
		categoryPlot = self.ui3.categoryBox.currentText()
		timePlot = self.ui3.categoryBox_2.currentText()

		UT.createPlot(typePlot, categoryPlot, timePlot, self.allData, self.figure)

		self.canvas.draw()

	def addHourAndUpdate(self, activity, add):
		self.actualState = UT.addHours(self.category, self.actualState, activity, add)
		self.levels = UT.getLevelFromData(self.actualState)
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)
		UT.setMainWin(self.ui, self.actualState, self.levels)

	def addHour1(self):
		self.addHourAndUpdate(activity=0, add=True)

	def addHour2(self):
		self.addHourAndUpdate(activity=1, add=True)

	def addHour3(self):
		self.addHourAndUpdate(activity=2, add=True)

	def minusHour1(self):
		self.addHourAndUpdate(activity=0, add=False)

	def minusHour2(self):
		self.addHourAndUpdate(activity=1, add=False)

	def minusHour3(self):
		self.addHourAndUpdate(activity=2, add=False)

	def click1(self, event):
		self.newWin()
		self.category = "Programming"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)

	def click2(self, event):
		self.newWin()
		self.category = "Reading"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)

	def click3(self, event):
		self.newWin()
		self.category = "Music"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)

	def click4(self, event):
		self.newWin()
		self.category = "Gaming"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)
	
	def click5(self, event):
		self.newWin()
		self.category = "Others"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)

	def click6(self, event):
		self.newWin()
		self.category = "Watched"
		UT.customLayout(self.ui2, self.category, self.levels, self.actualState)
	
	def saveEntries(self):
		#Add changes and update database
		self.ui.labelCheckEntry.setStyleSheet("color: rgb(72, 217, 0)")
		changesAdded = UT.calculateChanges(self.actualState, self.initalStateSave)
		allDataUpdated = UT.updateDatabase(self.allData, changesAdded)
		df = pd.DataFrame(data=allDataUpdated)
		df.to_excel(self.fileData, index=False)

		#Reset values
		self.allData, self.levels, self.actualState = self.loadData()
		self.initalStateSave = self.actualState.copy()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainwindow = MainWindow()
	widget = QtWidgets.QStackedWidget()
	widget.addWidget(mainwindow)
	widget.show()
	widget.setFixedWidth(791)
	widget.setFixedHeight(720)
	sys.exit(app.exec_())