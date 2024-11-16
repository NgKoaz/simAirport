import simpy
from .Checkpoint import Checkpoint
from .BoardingGate import BoardingGate

class CheckpointBuilder:
    def __init__(self):
        self.checkinCps = []
        self.securityCps = []
        self.boardingCps = []

    def build(self, env: simpy.Environment):
        return {
            "check-in": [Checkpoint(env, numStaff, serviceTime, isFirstClass) for (isFirstClass, numStaff, serviceTime) in self.checkinCps],
            "security": [Checkpoint(env, numStaff, serviceTime, isFirstClass) for (isFirstClass, numStaff, serviceTime) in self.securityCps],
            "boarding": [BoardingGate(env, numStaff, serviceTime, isFirstClass, gateId, timeStart) for (isFirstClass, numStaff, serviceTime, gateId, timeStart) in self.boardingCps],
        }

    def addCheckinCps(self, isFirstClass: bool, numStaff: int, serviceTime: float) -> 'CheckpointBuilder':
        self.checkinCps.append((isFirstClass, numStaff, serviceTime))
        return self

    def addSecurityCps(self, isFirstClass: bool, numStaff: int, serviceTime: float) -> 'CheckpointBuilder':
        self.securityCps.append((isFirstClass, numStaff, serviceTime))
        return self

    def addBoardingCps(self, isFirstClass: bool, numStaff: int, serviceTime: float, gateId: str, timeStart: float) -> 'CheckpointBuilder':
        self.boardingCps.append((isFirstClass, numStaff, serviceTime, gateId, timeStart))
        return self

