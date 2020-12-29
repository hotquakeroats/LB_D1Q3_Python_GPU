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
        
        self.ui.lineEditN1Liquid.editingFinished.connect(self.update_n1Liquid)
        self.ui.lineEditN1Vapor.editingFinished.connect(self.update_n1Vapor)
        self.ui.lineEditOmega.editingFinished.connect(self.update_oneOverTau)
        self.ui.lineEditAmp.editingFinished.connect(self.update_amp)
        self.ui.lineEditTc.editingFinished.connect(self.update_tc)
        self.ui.lineEditN0.editingFinished.connect(self.update_n0)
        self.ui.lineEditNc.editingFinished.connect(self.update_nc)
        self.ui.lineEditT0.editingFinished.connect(self.update_T0)
        self.ui.lineEditPc.editingFinished.connect(self.update_pc)
        self.ui.lineEditTheta.editingFinished.connect(self.update_theta)
        self.ui.lineEditG.editingFinished.connect(self.update_g)
        self.ui.lineEditLambda.editingFinished.connect(self.update_lmbda)
        self.ui.lineEditA1.editingFinished.connect(self.update_a1)
        self.ui.lineEditB1.editingFinished.connect(self.update_b1)
        self.ui.lineEditGammaP.editingFinished.connect(self.update_gammaP) #lambda : lbg.update_gammaP(float(self.ui.lineEditGammaP.text())))
        self.ui.lineEditGammaMu.editingFinished.connect(self.update_gammaMu)
        self.ui.lineEditKappa.editingFinished.connect(self.update_kappa)
        self.ui.lineEditHoldychCorrection.editingFinished.connect(self.update_pressureMethodCoefficient)
        self.ui.lineEditLaplaceCorrection.editingFinished.connect(self.update_pressureMethodCorrection)

    #
    # Update functions... either update UI display or update global variable values based on GUI inputs
    #
    
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
        
    def select_gradMu_forcing(self):
        lbg.useChemicalPotentialNonIdeal = not lbg.useChemicalPotentialNonIdeal
                   
    # TODO: want to move these "setter" functions to LB_globals eventually...
    def update_n1Liquid(self):
        lbg.n1_liquid = float(self.ui.lineEditN1Liquid.text())
    def update_n1Vapor(self):
        lbg.n1_vapor = float(self.ui.lineEditN1Vapor.text())
    def update_oneOverTau(self):
        lbg.oneOverTau = float(self.ui.lineEditOmega.text())
    def update_amp(self):
        lbg.Amp = float(self.ui.lineEditAmp.text())
    def update_tc(self):
        lbg.tc = float(self.ui.lineEditTc.text())
    def update_n0(self):
        lbg.n0 = float(self.ui.lineEditN0.text())
    def update_nc(self):
        lbg.nc = float(self.ui.lineEditNc.text())
    def update_T0(self):
        lbg.T0 = float(self.ui.lineEditT0.text())
    def update_pc(self):
        lbg.pc = float(self.ui.lineEditPc.text())
    def update_theta(self):
        lbg.theta = float(self.ui.lineEditTheta.text())
    def update_g(self):
        lbg.g = float(self.ui.lineEditG.text())
    def update_lmbda(self):
        lbg.lmbda = float(self.ui.lineEditLambda.text())
    def update_a1(self):
        lbg.a1 = float(self.ui.lineEditA1.text())
    def update_b1(self):
        lbg.b1 = float(self.ui.lineEditB1.text())
    def update_gammaP(self):
        lbg.gammaP = float(self.ui.lineEditGammaP.text())
    def update_gammaMu(self):
        lbg.gammaMu = float(self.ui.lineEditGammaMu.text())
    def update_kappa(self):
        lbg.kappa = float(self.ui.lineEditKappa.text())
    def update_pressureMethodCoefficient(self):
        lbg.pressureMethodCoefficient = float(self.ui.lineEditHoldychCorrection.text())
    def update_pressureMethodCorrection(self):
        lbg.pressureMethodCorrection = float(self.ui.lineEditLaplaceCorrection.text())
        
    #
    # Initialization functions
    #
                
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
        
    #
    # LB iteration control
    #

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
