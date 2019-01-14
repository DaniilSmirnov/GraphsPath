from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

matrix = []

class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('S Plot')

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.label_2 = QLabel("Матрица смежности")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 4, 1)
        self.tableWidget = QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 2)
        self.label = QLabel("Количество вершин")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.spinBox = QSpinBox()
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 2, 1, 1, 1)
        self.label_3 = QLabel("Путь:")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas, 0, 3, 9, 9)

        self.spinBox.valueChanged.connect(self.matrix_draw)
        self.tableWidget.cellChanged.connect(self.get_matrix)

        self.show()
        #self.plot3()

    def matrix_draw(self):
        amount = int(self.spinBox.text())
        i = 1
        self.tableWidget.setRowCount(amount)
        self.tableWidget.setColumnCount(amount)
        headers = []
        while i < amount:
            headers.append(str(i))
            i += 1
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setVerticalHeaderLabels(headers)

    def get_matrix(self):
        amount = int(self.spinBox.text())

        exec = True
        i = 1
        j = 1
        while i < amount:
            while j < amount:
                item = self.tableWidget.itemAt(i, j)
                if item.text() == "":
                    exec = False
                j += 1
            i += 1

        if exec:
            i = 1
            j = 1
            while i < amount:
                while j < amount:
                    item = self.tableWidget.itemAt(i, j)
                    print(item.text())
                    if int(item.text()) == 1:
                        matrix.append((i, j))
                    j += 1
                i += 1

        self.plot()


    def plot(self):
        self.figure.clf()
        G = nx.Graph()
        G.add_edges_from(matrix)
        nx.draw(G)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = MainWidget()
    screen.show()
    sys.exit(app.exec_())
