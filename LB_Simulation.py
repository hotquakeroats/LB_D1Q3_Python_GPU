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
        self.connect_controls()
        self.init_ui_vars()
        
        self.threadpool = QtCore.QThreadPool()
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui_vars)
        timer.start(33) # 33 ms update rate
        
    def connect_controls(self):
        self.ui.stepButton.clicked.connect(self.discrete_step)
        self.ui.startSimButton.clicked.connect(self.iterate_step)
        self.ui.initializeButton.clicked.connect(self.init_sim)
        
    def init_ui_vars(self):
        self.ui.lineEditStepSize.setText(str(LB_globals.step_size))
        self.ui.lineEditIterSize.setText(str(LB_globals.iter_size))
        
        self.ui.lineEditN1Liquid.setText(str(LB_globals.n1_liquid))
        self.ui.lineEditN1Vapor.setText(str(LB_globals.n1_vapor))
        
    def update_ui_vars(self):
        self.ui.lcdIterations.display(LB_globals.iterations)    # TODO: (maybe?) crashes @ 2.147 billion
        self.update_run_sim_button()
        
    def update_run_sim_button(self):
        if (LB_globals.iterations > 0):
            if (LB_globals.run_sim):            
                self.ui.startSimButton.setText("Pause Simulation") 
            else:
                self.ui.startSimButton.setText("Resume Simulation")
                
    def init_sim(self):
        LB_globals.iter_stop = 0
        LB_globals.iterations = 0
        self.ui.startSimButton.setText("Start Simulation") 
        
    def discrete_step(self):
        LB_globals.step_size = int(self.ui.lineEditStepSize.text())
        LB_globals.iterations += LB_globals.step_size
        
    def iterate_step(self):
        LB_globals.iter_size = int(self.ui.lineEditIterSize.text())        
        if LB_globals.iterations > LB_globals.iter_stop:    # catch if step above the stop
            LB_globals.iter_stop = LB_globals.iterations
        LB_globals.iter_stop += LB_globals.iter_size    # set for the next chunk of iterations
                
        # TODO: Is a new thread created with each click??        
        step_iterator = LB_Iteration()
        self.threadpool.start(step_iterator)
            
            
class LB_Iteration(QtCore.QRunnable):
    
#     def __init__(self):    # this isn't needed until I override the parent/QRunnable __init__
#         super().__init__()
    
    @QtCore.pyqtSlot()
    def run(self):
        LB_globals.run_sim = True if LB_globals.run_sim == False else False # toggle every button press
        while(LB_globals.run_sim):
            if (LB_globals.iterations >= LB_globals.iter_stop):
                LB_globals.run_sim = False
            else: 
                LB_globals.iterations += 1
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lb_simulation = LB_Simulation()
    lb_simulation.show()

    sys.exit(app.exec_())
