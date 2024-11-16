import simpy
from typing import Callable
from .Checkpoint import Checkpoint

class CheckpointBuilder:
    def __init__(self):
        self.checkinCps = []
        self.securityCps = []
        self.boardingCps = []

    def build(self, env: simpy.Environment):
        return {
            "check-in": [Checkpoint(env, numStaff, getServiceTime, isFirstClass) for (isFirstClass, numStaff, getServiceTime) in self.checkinCps],
            "security": [Checkpoint(env, numStaff, getServiceTime, isFirstClass) for (isFirstClass, numStaff, getServiceTime) in self.securityCps],
            "boarding": [Checkpoint(env, numStaff, getServiceTime, isFirstClass) for (isFirstClass, numStaff, getServiceTime) in self.boardingCps],
        }

    def addCheckinCps(self, isFirstClass: bool, numStaff: int, getServiceTime: Callable) -> 'CheckpointBuilder':
        self.checkinCps.append((isFirstClass, numStaff, getServiceTime))
        return self

    def addSecurityCps(self, isFirstClass: bool, numStaff: int, getServiceTime: Callable) -> 'CheckpointBuilder':
        self.securityCps.append((isFirstClass, numStaff, getServiceTime))
        return self

    def addBoardingCps(self, isFirstClass: bool, numStaff: int, getServiceTime: Callable) -> 'CheckpointBuilder':
        self.boardingCps.append((isFirstClass, numStaff, getServiceTime))
        return self

