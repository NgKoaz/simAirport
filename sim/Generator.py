import simpy
import random

from .Passenger import Passenger
from .CheckpointManager import CheckpointManager

class Generator:
    def __init__(self, env: simpy.Environment, cpManager: CheckpointManager, interArrivalTime: float, rateFirstClass: float) -> None:
        self.env = env
        self.cpManager = cpManager
        self.interArrivalTime = interArrivalTime
        self.rateFirstClass = rateFirstClass
    
    def _getRandomIntervalTime(self) -> float:
        return random.expovariate(1.0 / self.interArrivalTime)
    
    def run(self):
        # 1. Create a new passenger
        # 2. Increase an ID for next passenger
        # 3. Time out, then back to number 1.
        while True:
            isPassengerFirstClass = random.random() > (1 - self.rateFirstClass)
            newPassenger = Passenger(self.env, self.cpManager, isPassengerFirstClass)
            self.env.process(newPassenger.run())
            yield self.env.timeout(self._getRandomIntervalTime())

    def generateBoardingGate(self):
        pass
    