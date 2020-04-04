import LB_GUI
import sys
import time

from LB_global_vars import *
from PyQt5 import QtWidgets, QtCore
import LB_global_vars


class LB_Simulation(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        self.ui = LB_GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui_vars()
        
        self.threadpool = QtCore.QThreadPool()
        self.done = False
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui_vars)
        timer.start(10) # 10 ms update rate
        
    def init_ui_vars(self):
        self.ui.lineEditStepSize.setText(str(LB_global_vars.step_size))
        self.ui.lineEditN1Liquid.setText(str(LB_global_vars.n1_liquid))
        self.ui.lineEditN1Vapor.setText(str(LB_global_vars.n1_vapor))
        
        self.ui.stepButton.clicked.connect(self.test_discrete_step)
        self.ui.startSimButton.clicked.connect(self.test_iterate_step)
        
    def update_ui_vars(self):
        self.ui.lcdIterations.display(LB_global_vars.iterations)
        
        if (LB_global_vars.iterations == 10000):
            self.done = True
        
    def test_discrete_step(self):
        LB_global_vars.iterations += LB_global_vars.step_size
        
    def test_iterate_step(self):
        step_iterator = self.LB_Iteration()
        self.threadpool.start(step_iterator)
            
            
class LB_Iteration(QtCore.QRunnable):
    
    @QtCore.pyqtSlot()
    def run(self):
        while(not self.done):
            print(str(LB_global_vars.iterations))
#             LB_global_vars.iterations += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lb_simulation = LB_Simulation()
    lb_simulation.show()

    sys.exit(app.exec_())
