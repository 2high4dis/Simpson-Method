from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFont

import pyqtgraph as pg
import numpy as np
from math import sqrt
import sys


def f(formula: str, x: int):
    formula = formula.replace('x', f'({x})')
    return eval(formula)


class Window(QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()

        # sizing and position

        self.width = 1000
        self.height = 525
        self.x = int((1920 - self.width) / 2)
        self.y = int((1080 - self.height) / 2)

        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowTitle('Simpson\'s Rule')
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet('font: 20px Times New Roman;')

        self.header = QtWidgets.QLabel(
            self, text='Integral calculation using Simpson\'s Method')
        self.header.setGeometry(0, 0, self.width, 40)
        self.header.setStyleSheet('''
                                    color: blue;
                                    border: 1px solid lightgrey;
                                    padding: 5px;
        ''')
        self.var_block = QtWidgets.QLabel(self)
        self.var_block.setGeometry(0, 40, 340, self.height - 40)
        self.var_block.setStyleSheet('''QLabel{
                                    border: 1px solid lightgrey;
        }''')
        self.section_label = QtWidgets.QLabel(
            self.var_block, text='Choose sections count: ')
        self.section_label.setGeometry(5, 5, 330, 30)
        self.section_label.setStyleSheet('border: none;')
        self.n_label = QtWidgets.QLabel(self.var_block, text='n = ')
        self.n_label.setGeometry(5, 45, 40, 30)
        self.n_label.setStyleSheet('border: none;')
        self.n_input = QtWidgets.QSpinBox(self.var_block)
        self.n_input.setMinimum(0)
        self.n_input.setGeometry(45, 45, 290, 30)

        self.limits_label = QtWidgets.QLabel(
            self.var_block, text='Enter an integral limits: ')
        self.limits_label.setGeometry(5, 85, 330, 30)
        self.limits_label.setStyleSheet('border: none;')
        self.a_label = QtWidgets.QLabel(self.var_block, text='a = ')
        self.a_label.setGeometry(5, 125, 40, 30)
        self.a_label.setStyleSheet('border: none;')
        self.a_input = QtWidgets.QSpinBox(self.var_block)
        self.a_input.setGeometry(45, 125, 290, 30)
        self.a_input.setMinimum(-100)
        self.b_label = QtWidgets.QLabel(self.var_block, text='b = ')
        self.b_label.setGeometry(5, 165, 40, 30)
        self.b_label.setStyleSheet('border: none;')
        self.b_input = QtWidgets.QSpinBox(self.var_block)
        self.b_input.setGeometry(45, 165, 290, 30)
        self.b_input.setMinimum(-99)
        self.b_input.setMaximum(100)

        self.function_label = QtWidgets.QLabel(
            self.var_block, text='Enter the subintegral function: ')
        self.function_label.setGeometry(5, 205, 330, 30)
        self.function_label.setStyleSheet('border: none;')
        self.fx_label = QtWidgets.QLabel(self.var_block, text='F(x) = ')
        self.fx_label.setGeometry(5, 245, 60, 30)
        self.fx_label.setStyleSheet('border: none;')
        self.fx_input = QtWidgets.QLineEdit(self.var_block)
        self.fx_input.setGeometry(65, 245, 270, 30)

        self.submit_button = QtWidgets.QPushButton(
            self.var_block, text='Calculate')
        self.submit_button.setGeometry(5, 285, 330, 40)
        self.clear_button = QtWidgets.QPushButton(self.var_block, text='Clear')
        self.clear_button.setGeometry(5, 330, 330, 40)

        self.ans_label = QtWidgets.QLabel(self.var_block, text='Answer: ')
        self.ans_label.setGeometry(5, 380, 330, 30)
        self.ans_label.setStyleSheet('border: none;')
        self.ans_output = QtWidgets.QLabel(self.var_block)
        self.ans_output.setGeometry(5, 420, 330, 30)
        self.ans_output.setStyleSheet('''background: white;
                                      border: 1px solid lightgrey;''')

        self.submit_button.clicked.connect(self.submit)
        self.clear_button.clicked.connect(self.clear)

        self.graph_block = QtWidgets.QLabel(self)
        self.graph_block.setGeometry(340, 40, 660, self.height - 40)
        self.graph_block.setStyleSheet('background: white;')
        self.graph = pg.PlotWidget(self.graph_block)
        self.graph.setGeometry(0, 0, 660, self.height - 40)
        self.graph.showGrid(x=True, y=True)
        self.graph.setTitle("F(x) Graph:", color=(0, 0, 0), size='24pt')
        self.graph.hide()

    def submit(self):
        self.graph.clear()
        n = self.n_input.value()

        a = self.a_input.value()
        b = self.b_input.value()

        h = (b - a) / n

        formula = self.fx_input.text()
        s = (h / 3) * (f(formula, a) + f(formula, b) + 4 *
                       sum(f(formula, i * h) for i in range(1, n, 2)) + 2 * sum(f(formula, j * h) for j in range(2, n - 1, 2)))

        x = np.arange(a, b + 0.02, 0.02)
        y = np.array([f(formula, item) for item in x])

        pen = pg.mkPen(color=(0, 0, 0), width=2)
        self.graph.setBackground('w')
        self.graph.plot(x, y, pen=pen)

        self.ans_output.setText(f'{s}')
        self.graph.show()

    def clear(self):
        self.n_input.setValue(0)
        self.a_input.setValue(0)
        self.b_input.setValue(0)
        self.fx_input.setText('')
        self.ans_output.setText('')
        self.graph.clear()
        self.graph.hide()


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    application()
