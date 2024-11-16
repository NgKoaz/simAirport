import simpy
from typing import List
from .Checkpoint import Checkpoint
from .CheckpointBuilder import CheckpointBuilder
from .BoardingGate import BoardingGate


class CheckpointManager:
    CHECK_IN = "check-in"
    SECURITY = "security"
    BOARDING = "boarding"

    def __init__(self, env: simpy.Environment, cpBuilder: CheckpointBuilder) -> None:
        self.env = env
        self.checkpoints = cpBuilder.build(env)
    
    def getBoardingGateList(self):
        gateIdList = {}
        cps: List[BoardingGate] = self.checkpoints[CheckpointManager.BOARDING]
        for cp in cps: 
            if cp.getGateId() not in gateIdList: 
                gateIdList[cp.getGateId()] = [cp]
            else: 
                gateIdList[cp.getGateId()].append(cp)
        return gateIdList
    
    def getCheckinCps(self) -> List[Checkpoint]:
        return self.checkpoints["check-in"]
    
    def getSecurityCps(self) -> List[Checkpoint]:
        return self.checkpoints["security"]
    
    def getBoardingCps(self) -> List[BoardingGate]:
        return self.checkpoints["boarding"]

    def _getShortestCps(self, cps: List[Checkpoint]) -> Checkpoint:
        return min(cps, key=lambda cp: cp.getNumWaiting())

    def _filter(self, cps: List[Checkpoint], isFirstClass: bool) -> List[Checkpoint]:
        return filter(lambda cp: cp.isFirstClass() == isFirstClass, cps)  

    def getProperCheckpoint(self, type: str, isFirstClass: bool) -> Checkpoint:
        # 1. Choose destination 
        # 2. Filter by isFirstClass
        # 3. Choose shortest queue 
        candidateCps = self.checkpoints[type]
        candidateCps = list(self._filter(candidateCps, isFirstClass))
        if len(candidateCps) <= 0:
            raise Exception("Passenger can't choose Checkpoint!")
        return self._getShortestCps(candidateCps)

    def getProperBoardingGate(self, earlyArrivalTime, isFirstClass: bool) -> BoardingGate:
        candidateCps = self.checkpoints[CheckpointManager.BOARDING] 
        candidateCps: List[BoardingGate] = list(self._filter(candidateCps, isFirstClass))
        if len(candidateCps) <= 0:
            raise Exception("Passenger can't choose Checkpoint!")
        return min(candidateCps, key=lambda cp: abs(cp.getTimeStart() - (self.env.now + earlyArrivalTime)))    
