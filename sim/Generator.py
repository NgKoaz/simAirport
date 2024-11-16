import simpy
import random
from typing import Callable

from .Passenger import Passenger
from .CheckpointManager import CheckpointManager

class Generator:
    def __init__(self, env: simpy.Environment, cpManager: CheckpointManager, getInterArrivalTime: Callable, rateFirstClass: float) -> None:
        self.env = env
        self.cpManager = cpManager
        self.getInterArrivalTime = getInterArrivalTime
        self.rateFirstClass = rateFirstClass
    
    def run(self):
        # 1. Create a new passenger
        # 2. Increase an ID for next passenger
        # 3. Time out, then back to number 1.
        while True:
            isPassengerFirstClass = random.random() > (1 - self.rateFirstClass)
            newPassenger = Passenger(self.env, self.cpManager, isPassengerFirstClass)
            self.env.process(newPassenger.run())
            yield self.env.timeout(self.getInterArrivalTime())

    