import time
from sim.Simulation import Simulation
from sim.CheckpointManager import *

cpBuilder = CheckpointBuilder()
cpBuilder.addCheckinCps(True, 1, 1)
cpBuilder.addCheckinCps(False, 1, 1)
cpBuilder.addCheckinCps(False, 1, 1)

cpBuilder.addSecurityCps(True, 1, 3)
cpBuilder.addSecurityCps(False, 1, 1)
cpBuilder.addSecurityCps(False, 1, 1)

cpBuilder.addBoardingCps(True, 1, 0.15)
cpBuilder.addBoardingCps(False, 1, 0.15)


sim = Simulation(interArrivalTime=1, cpBuilder=cpBuilder, randomSeed=int(time.time()), rateFirstClass=0.05)
sim.run(until=200)