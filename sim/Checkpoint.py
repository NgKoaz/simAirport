import simpy
import random

class Checkpoint:
    NextId = 0

    def __init__(self, env: simpy.Environment, numStaff: int, serviceTime: float, isFirstClass: bool) -> None:
        self.env = env
        self._isFirstClass = isFirstClass
        self.staffs = simpy.Resource(env, numStaff)
        self.serviceTime = serviceTime
        self.data = []
        Checkpoint.NextId += 1

    def getStaffs(self) -> simpy.Resource:
        return self.staffs

    def getServingTime(self) -> float:
        return random.expovariate(1.0 / self.serviceTime)

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
            mu = self.getServingTime()
            # print(f"Checkpoint has random service time {mu} and mean of service time: {self.serviceTime}")
            yield self.env.timeout(mu) 
        self.onPassengerLeave(passenger)

    def onPassengerArrive(self, passenger):
        # Record data
        pass

    def onPassengerLeave(self, passenger):
        # Record data
        pass
    
