import cProfile
import LB_collisions
import LB_globals as lbg
import LB_GUI
import LB_Initialize
import pyqtgraph
import sys

from PyQt5 import QtWidgets, QtCore


class LB_Simulation(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        pyqtgraph.setConfigOptions(useOpenGL=True, antialias=True)
        self.density_plot = None
        
        self.ui = LB_GUI.Ui_MainWindow()
        self.ui.setupUi(self)        
        self.connect_controls()
        lbg.init_ui_vars(self.ui)
        self.init_sim()
        
        self.threadpool = QtCore.QThreadPool()
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui_vars)
        timer.start(33) # 30 Hz update rate
        
    def connect_controls(self):
        self.ui.stepButton.clicked.connect(lambda : self.iterate_step(int(self.ui.lineEditStepSize.text())))
        self.ui.startSimButton.clicked.connect(lambda : self.iterate_step(None))
        self.ui.initializeButton.clicked.connect(self.init_sim)

        
        # Trap toggle of 1 button from 2-button group to initialize density profile
        self.ui.radioDensityProfileRandom.toggled.connect(self.init_density_profile)
        
        # Read radio buttons to choose collision algorithm
        self.ui.radioForceNewGradMu.clicked.connect(lambda : LB_collisions.set_collision("collisionForcingNewChemicalPotentialGradient"))
        self.ui.radioForceNewGradP.clicked.connect(lambda : LB_collisions.set_collision("collisionForcingNewPressureGradient")) 
        self.ui.radioPressureMethod.clicked.connect(lambda : LB_collisions.set_collision("collisionPressureMethod"))

        # Grad-Mu NID or Log method
        self.ui.radioChemPotLogMethod.toggled.connect(self.select_gradMu_forcing)

        
    def update_ui_vars(self):
        self.ui.lcdIterations.display(lbg.iterations)    # TODO: (maybe fix?) crashes @ 2.147 billion
        self.update_run_sim_button()
        self.update_density_plot()
        
    def update_run_sim_button(self):
        if (lbg.iterations > 0):
            if (lbg.run_sim):            
                self.ui.startSimButton.setText("Pause Simulation") 
            else:
                self.ui.startSimButton.setText("Resume Simulation")
                
    def update_density_plot(self):
        self.density_plot.setData(lbg.x_axis_labels, lbg.n1)
                
    def init_sim(self):
        lbg.iter_stop = 0
        lbg.iterations = 0
        LB_Initialize.initialize()

        self.ui.widgetDensityPlot.setXRange(0, lbg.XDIM, padding=0)
        self.ui.widgetDensityPlot.setYRange(0, 2, padding=0)
        self.ui.widgetDensityPlot.clear()
        self.density_plot = self.ui.widgetDensityPlot.plot()
        
        self.ui.startSimButton.setText("Start Simulation")
        
    def init_density_profile(self):
        lbg.useDensityProfileStep = not lbg.useDensityProfileStep
        self.init_sim()
        
    def select_gradMu_forcing(self):
        lbg.useChemicalPotentialNonIdeal = not lbg.useChemicalPotentialNonIdeal

    def iterate_step(self, step_size):
        if lbg.iterations > lbg.iter_stop:    # catch if step above the stop
            lbg.iter_stop = lbg.iterations
            
        if step_size is not None:
            lbg.useStepStop = True
            lbg.iter_stop += step_size    # set for the next chunk of iterations        
        
        # TODO: Is a new thread created with each click??        
        step_iterator = LB_Iteration()
        self.threadpool.start(step_iterator)
            
            
class LB_Iteration(QtCore.QRunnable):
  
#     def __init__(self):    # this isn't needed until I override the parent/QRunnable __init__
#         super().__init__()
    
    @QtCore.pyqtSlot()
    def run(self):
#         profile = cProfile.Profile()
#         profile.enable()
        lbg.run_sim = True if lbg.run_sim == False else False # toggle every button press
        while(lbg.run_sim):
            if (lbg.useStepStop and lbg.iterations >= lbg.iter_stop):
                lbg.run_sim = False
                lbg.useStepStop = False
            else: 
                lbg.iterations += 1
                LB_collisions.iteration()
#         profile.disable()
#         profile.print_stats(sort='time')        
 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lb_simulation = LB_Simulation()
    lb_simulation.show()
    sys.exit(app.exec_())
