import simpy
from typing import Callable

from .Generator import Generator
from .CheckpointManager import *
from .CheckpointBuilder import CheckpointBuilder

class Simulation:
    def __init__(self, getInterArrivalTime: Callable, cpBuilder: CheckpointBuilder, rateFirstClass: float) -> None:
        self.env = simpy.Environment()
        self.cpManager = CheckpointManager(self.env, cpBuilder)
        self.generator = Generator(self.env, self.cpManager, getInterArrivalTime, rateFirstClass)
        self._prepare()

    def _prepare(self) -> None:
        self.env.process(self.generator.run())

    def run(self, until):
        self.env.run(until=until)
