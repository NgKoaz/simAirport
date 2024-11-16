import time
import random
from sim.Simulation import Simulation
from sim.CheckpointManager import *


# GLOBAL VARIABLE
CHECK_IN_NUM_STAFF = 4
SECURITY_NUM_STAFF = 4
BOARDING_GATE_NUM_STAFF = 1

CHECK_IN_SERVICE_TIME = 30
SECURITY_SERVICE_TIME = 20
BOARDING_GATE_SERVICE_TIME = 10


# Seed takes current time of computer. 
# Frequently change. You can choose a fixed number, fixed number will fix result. Example: random.seed(123)
random.seed(time.time())

def generateServiceTime():
    return random.expovariate(1.0 / CHECK_IN_SERVICE_TIME)

# Build checkpoints
cpBuilder = CheckpointBuilder()
cpBuilder.addCheckinCps(True, CHECK_IN_NUM_STAFF, lambda: random.expovariate(1.0 / CHECK_IN_SERVICE_TIME))
cpBuilder.addCheckinCps(False, CHECK_IN_NUM_STAFF, lambda: random.expovariate(1.0 / CHECK_IN_SERVICE_TIME))
cpBuilder.addSecurityCps(True, SECURITY_NUM_STAFF, lambda: random.expovariate(1.0 / CHECK_IN_SERVICE_TIME))
cpBuilder.addSecurityCps(False, SECURITY_NUM_STAFF, lambda: random.expovariate(1.0 / CHECK_IN_SERVICE_TIME))
cpBuilder.addBoardingCps(True, BOARDING_GATE_NUM_STAFF, generateServiceTime)
cpBuilder.addBoardingCps(False, BOARDING_GATE_NUM_STAFF, generateServiceTime)


# Initialize Simulation
sim = Simulation(
    getInterArrivalTime=lambda: random.expovariate(1.0 / 5.0), 
    cpBuilder=cpBuilder, 
    rateFirstClass=0.05
)
sim.run(until=200)








# Class structure:
# Simulation
#   CheckpointManager
#       Checkpoint
#   Generator
#       Passenger

# Process: (Generator process will produce passenger process)
# Generator.run()
#   Passenger.run()
