import simpy
import random

from .Generator import Generator
from .CheckpointManager import *
from .CheckpointBuilder import CheckpointBuilder

class Simulation:
    def __init__(self, interArrivalTime: int, cpBuilder: CheckpointBuilder, randomSeed: int, rateFirstClass: float) -> None:
        self.env = simpy.Environment()
        self.cpManager = CheckpointManager(self.env, cpBuilder)
        self.generator = Generator(self.env, self.cpManager, interArrivalTime, rateFirstClass)
        random.seed(randomSeed)
        self._prepare()

    def _prepare(self) -> None:
        self.env.process(self.generator.run())

    def run(self, until):
        self.env.run(until=until)


# Generator process
    # => Passerger processes
    # => Boarding Gate processes
# Observer process