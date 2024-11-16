import simpy
from typing import Callable

class Checkpoint:
    NextId = 0

    def __init__(self, env: simpy.Environment, numStaff: int, getServiceTime: Callable, isFirstClass: bool) -> None:
        self.env = env
        self._isFirstClass = isFirstClass
        self.staffs = simpy.Resource(env, numStaff)
        self.getServiceTime = getServiceTime
        Checkpoint.NextId += 1

    def getStaffs(self) -> simpy.Resource:
        return self.staffs

    def isFirstClass(self) -> bool:
        return self._isFirstClass
    
    def getNumWaiting(self) -> int:
        return len(self.staffs.queue)

    def getTotalInside(self) -> int:
        return self.staffs.count + len(self.staffs.queue)
    
    def serve(self, passenger):
        self.onPassengerArrive(passenger)
        with self.staffs.request() as req:
            yield req
            mu = self.getServiceTime()
            # print(f"Checkpoint has random service time {mu} and mean of service time: {self.serviceTime}")
            yield self.env.timeout(mu) 
        self.onPassengerLeave(passenger)

    def onPassengerArrive(self, passenger):
        # Record data
        pass

    def onPassengerLeave(self, passenger):
        # Record data
        pass
    
