import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Organiser')

        self.win = QtWidgets.QWidget()
        self.layout = QtWidgets.QFormLayout()

        # You can't really extract data 
        # from the layout. You can predefine
        # the widgets though.
        self.name = QtWidgets.QLineEdit()
        self.surname = QtWidgets.QLineEdit()
        self.pet_name = QtWidgets.QLineEdit()
        self.get_data_b = QtWidgets.QPushButton('get data')
        self.get_data_b.clicked.connect(self.get_data)

        # and use them here
        self.layout.addRow(QtWidgets.QLabel("Name:"), self.name)
        self.layout.addRow(QtWidgets.QLabel("Surname:"), self.surname)
        self.layout.addRow(QtWidgets.QLabel("Pet Name:"), self.pet_name)
        self.layout.addRow(self.get_data_b)

        self.win.setLayout(self.layout)
        self.setCentralWidget(self.win)

    def get_data(self):
        print(self.name.text())
        print(self.surname.text())
        print(self.pet_name.text())


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()