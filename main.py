import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

matrix = []


class MainWidget(QWidget):

    def __init__(self):
        super(MainWidget, self).__init__()
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.center()
        self.setWindowTitle('Поиск Эйлерова пути')

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
        self.tableWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
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
        self.gridLayout.addWidget(self.canvas, 0, 3, 4, 1)

        self.spinBox.valueChanged.connect(self.matrix_draw)
        self.tableWidget.cellChanged.connect(self.get_matrix)

        self.spinBox.setValue(2)
        self.show()

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
        self.tableWidget.resizeColumnsToContents()

    def get_matrix(self):
        amount = int(self.spinBox.text())

        exec = True

        for i in range(0, amount, 1):
            for j in range(0, amount, 1):
                item = self.tableWidget.item(i, j)
                if item is None:
                    exec = False
                j += 1
            i += 1

        if exec:
            for i in range(0, amount, 1):
                for j in range(0, amount, 1):
                    item = self.tableWidget.item(i, j)
                    if item.text() == "1":
                        matrix.append((i+1, j+1))

                    j += 1
                i += 1

            self.plot()

    def plot(self):
        self.figure.clf()
        G = nx.Graph()
        G.add_edges_from(matrix)
        nx.draw(G, with_labels=True)
        self.canvas.draw_idle()

        try:
            self.label_3.setText("Эйлеров путь для введеного графа: " + str(list(nx.eulerian_circuit(G))))
        except nx.NetworkXError:
            self.label_3.setText("В этом графе Эйлерова пути не существует")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle("Fusion")
    screen = MainWidget()
    screen.show()
    sys.exit(app.exec_())
