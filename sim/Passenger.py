import simpy
import random

from .CheckpointManager import CheckpointManager
from .Checkpoint import Checkpoint
from .Destination import Destination

class Passenger:
    NextId = 0

    def __init__(self, env: simpy.Environment, cpManager: CheckpointManager, isFirstClass: bool) -> None:
        self.env = env
        self.id = Passenger._getNewId()
        self.dest = Destination.START
        self.cpManager = cpManager
        self.isFirstClass = isFirstClass

        self.onPassengerArriveAirport()

    @staticmethod
    def _getNewId() -> int:
        curId = Passenger.NextId
        Passenger.NextId += 1
        return curId

    def getDestination(self):
        return self.dest

    def getTimePassengerArriveInAdvance(self):
        return random.gauss(90, 30)

    def _nextDestination(self) -> bool:
        self.dest += 1
        return self.dest != Destination.FINISH

    def _chooseCheckpoint(self) -> Checkpoint: 
        if self.dest == Destination.CHECK_IN:
            return self.cpManager.getProperCheckpoint(CheckpointManager.CHECK_IN, self.isFirstClass)
        elif self.dest == Destination.SECURITY:
            return self.cpManager.getProperCheckpoint(CheckpointManager.SECURITY, self.isFirstClass)
        elif self.dest == Destination.BOARDING:
            earlyArrivalTime = self.getTimePassengerArriveInAdvance()
            return self.cpManager.getProperBoardingGate(earlyArrivalTime, self.isFirstClass)
        raise Exception("[Error] Wrong logic!")

    def run(self):
        while self._nextDestination():
            cp = self._chooseCheckpoint()
            # self.onPassengerEnterCheckpoint()
            yield from cp.serve(self)
            # self.onPassengerLeaveCheckpoint()
        # self.onPassengerLeaveAirport()    

    def onPassengerArriveAirport(self):
        pass
        # print(f"Passenger has id {self.id} has been created! At: {self.env.now}")

    def onPassengerLeaveAirport(self):
        pass
        # print(f"Passenger has id {self.id} has left! At: {self.env.now}")

    def onPassengerEnterCheckpoint(self):
        pass
        # print(f"Passenger has id {self.id} has entered into a checkpoint! At: {self.env.now}")

    def onPassengerLeaveCheckpoint(self):
        pass
        # print(f"Passenger has id {self.id} has left into a checkpoint! At: {self.env.now}")

        