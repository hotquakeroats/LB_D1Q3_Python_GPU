import LB_globals
import LB_GUI
import sys
import time

# from LB_globals import *
from PyQt5 import QtWidgets, QtCore


class LB_Simulation(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        self.ui = LB_GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui_vars()
        
        self.threadpool = QtCore.QThreadPool()
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui_vars)
        timer.start(33) # 33 ms update rate
        
        self.test_stop = 0
        
    def init_ui_vars(self):
        self.ui.lineEditStepSize.setText(str(LB_globals.step_size))
        self.ui.lineEditN1Liquid.setText(str(LB_globals.n1_liquid))
        self.ui.lineEditN1Vapor.setText(str(LB_globals.n1_vapor))
        
        self.ui.stepButton.clicked.connect(self.discrete_step)
        self.ui.startSimButton.clicked.connect(self.iterate_step)
        
    def update_ui_vars(self):
        self.ui.lcdIterations.display(LB_globals.iterations)
        
    def discrete_step(self):
        LB_globals.iterations += LB_globals.step_size
        
    def iterate_step(self):
        step_iterator = LB_Iteration()
        self.threadpool.start(step_iterator)
            
            
class LB_Iteration(QtCore.QRunnable):
    
#     def __init__(self):    # this isn't needed until I override the parent/QRunnable __init__
#         something_else...
#         super().__init__()
    
    @QtCore.pyqtSlot()
    def run(self):
        while(not LB_globals.done):
            if (LB_globals.iterations == 10000000):
                LB_globals.done = True
            else: 
                LB_globals.iterations += 1
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lb_simulation = LB_Simulation()
    lb_simulation.show()

    sys.exit(app.exec_())
