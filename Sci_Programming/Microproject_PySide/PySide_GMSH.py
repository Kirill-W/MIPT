import gmsh
import sys
import numpy as np

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui


lc = 1e-2
EXIT_CODE_REBOOT = -11231351

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
    
        gmsh.initialize()

        gmsh.model.add("t1")
    
        self.arr_1 = [] # Массив массивов-координат
        self.arr_3 = [] # Массив номеров loop'ов
        self.arr_4 = [] # Массив номеров линий
        self.k = 1  # Счётчик точек
        self.l = 1  # Счётчик line'ов
        self.CL = 1 # Счётчик curve loop'ов
        self.points_1 = 'Added Points: \n'
        self.loops_1 = 'Added Loops: \n'
    
        super().__init__(parent)
        self.setWindowTitle('PySide - GMSH')

        self.win = QtWidgets.QWidget()
        self.layout = QtWidgets.QFormLayout()

        self.coord = QtWidgets.QLineEdit()
        self.loop = QtWidgets.QLineEdit()
        
        self.get_data_b = QtWidgets.QPushButton('Upload Coordinates')  # Предварительно загрузить координаты
        self.get_data_b.clicked.connect(self.get_data) 
        self.coord.returnPressed.connect(self.get_data)  # Срабатывает при нажатии на Enter
        
        self.pr_data_b = QtWidgets.QPushButton('Convert Coordinates into Points') # Из координат в точки GMSH
        self.pr_data_b.clicked.connect(self.process_data)
        
        self.get_data_l = QtWidgets.QPushButton('Upload Loop Sequence') # Загрузить кривую - последовательность точек
        self.get_data_l.clicked.connect(self.get_loop)       
        self.loop.returnPressed.connect(self.get_loop)  # Срабатывает при нажатии на Enter
        
        self.mesh = QtWidgets.QPushButton('Create Mesh') # Делаем сетку
        self.mesh.clicked.connect(self.create_mesh)
        
        self.restart = QtWidgets.QPushButton('Restart') # Перезапускаем
        self.restart.clicked.connect(self.do_restart)

        self.layout.addRow(QtWidgets.QLabel("Enter Point Coordinates:"), self.coord)
        self.layout.addRow(QtWidgets.QLabel("Enter Points You Want to Loop in Curve:"), self.loop)

        self.layout.addRow(self.get_data_b)
        self.layout.addRow(self.pr_data_b)
        self.layout.addRow(self.get_data_l)
        self.layout.addRow(self.mesh)
        self.layout.addRow(self.restart)
        

        self.win.setLayout(self.layout)
        self.setCentralWidget(self.win)
        
        
        self.SA = QtWidgets.QScrollArea()
        self.SA.setGeometry(QtCore.QRect(12, 180, 100, 179))
        self.SA.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SA.setObjectName("SA")
        self.SA.setWidgetResizable(True)
        self.SA.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SA.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.SA.setWidget(self.win)
        
        self.setCentralWidget(self.SA)


    def get_data(self):  # Считать координаты
        
        self.arr_1.append(np.fromstring(self.coord.text(), dtype=float, sep=' '))
        self.coord.clear()

        
    def process_data(self):  # Координаты в точки GMSH
    
        self.points = self.points_1
        
        for i in range(self.k - 1, len(self.arr_1)):
            gmsh.model.geo.addPoint(self.arr_1[i][0], self.arr_1[i][1], self.arr_1[i][2], lc, self.k)
            self.points += "{}:     ({}     {}      {})\n".format(self.k, self.arr_1[i][0], self.arr_1[i][1], self.arr_1[i][2])
            self.k += 1
         
        self.text_p = QtWidgets.QLabel(self.points, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text_p)

            
    def get_loop(self):  # Последовательность номеров точек - в линии, curve loop'ы, plane surface'ы
    
        self.loops = self.loops_1
    
        self.arr_2 = np.fromstring(self.loop.text(), dtype=int, sep=' ')
        self.arr_2 = np.append(self.arr_2, self.arr_2[0])
        
        for j in range(len(self.arr_2) - 1):  # Называем линии так, чтобы 3->1 было -(1->3), если 1->3 уже встречалось и т.п.
            if ((self.arr_2[j]*10 + self.arr_2[j + 1]) in self.arr_4):
                self.arr_3.append(self.arr_2[j]*10 + self.arr_2[j + 1])
                
            elif ((self.arr_2[j + 1]*10 + self.arr_2[j]) in self.arr_4):
                self.arr_3.append(-self.arr_2[j + 1]*10 - self.arr_2[j])
                
            else:
                gmsh.model.geo.addLine(self.arr_2[j], self.arr_2[j + 1], self.arr_2[j]*10 + self.arr_2[j + 1])
                self.arr_3.append(self.arr_2[j]*10 + self.arr_2[j + 1])
                self.arr_4.append(self.arr_2[j]*10 + self.arr_2[j + 1])
        
        gmsh.model.geo.addCurveLoop(self.arr_3, self.CL)
        gmsh.model.geo.addPlaneSurface([self.CL], self.CL)
            
        self.loops += "{}:     ({})\n".format(self.CL, self.arr_2)
        
        self.CL += 1
        
        self.arr_3 = []

        self.text_l = QtWidgets.QLabel(self.loops, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text_l)        
        
        self.loop.clear()
 
 
    def create_mesh(self):  # Создание surface loop, объёма, сетки
    
        try:
            v = gmsh.model.geo.addSurfaceLoop([i + 1 for i in range(self.CL - 1)])
            gmsh.model.geo.addVolume([v])
        
            gmsh.model.geo.synchronize()

            gmsh.model.mesh.generate(3)
         
        except:
            gmsh.model.geo.synchronize()
            
            gmsh.model.mesh.generate(2)

        gmsh.write("t1.msh")
        gmsh.write("t1.geo_unrolled")
        gmsh.write("t1.vtk")

        if '-nopopup' not in sys.argv:
            gmsh.fltk.run()

        gmsh.finalize()
        
    def do_restart(self):  # Перезапуск
    
        return QtCore.QCoreApplication.exit( EXIT_CODE_REBOOT )
    

def main():

    exit_code = 0
    while True:
        try:
            app = QtWidgets.QApplication(sys.argv)
        except RuntimeError:
            app = QtCore.QCoreApplication.instance()
            
        win = MainWindow()
        win.resize(600, 500)
        win.show()            
        
        exit_code = app.exec_()          
        
        if exit_code != EXIT_CODE_REBOOT:
            break        
            
    return exit_code


if __name__ == '__main__':
    main()
