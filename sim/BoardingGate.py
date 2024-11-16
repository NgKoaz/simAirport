import simpy
import random
import math
from .Checkpoint import Checkpoint
from .Destination import Destination


class BoardingGate(Checkpoint):
    BreakInterval = 60
    OpenInterval = 35

    def __init__(self, env: simpy.Environment, numStaff: int, serviceTime: float, isFirstClass: bool, gateId: str, timeStart: float) -> None:
        super().__init__(env=env, numStaff=numStaff, serviceTime=serviceTime, isFirstClass=isFirstClass)
        self.gateId = gateId
        self.timeStart = timeStart
        self.openEvent = self.env.event()

    def getGateId(self) -> str:
        return self.gateId

    def getTimeStart(self):
        return self.timeStart

    def getServingTime(self) -> float:
        return random.expovariate(1.0 / self.serviceTime)

    # In Boarding Gate's process
    def run(self):
        while True:
            # print(max(0, self.timeStart - self.env.now))
            # 1. Timeout until open the gate
            # 2. Trigger event to passengers come in.
            # 3. Open in 30 min.
            # 4. Close
            # 5. Renew timeStart, open time, back to 1.
            yield self.env.timeout(max(0, self.timeStart - self.env.now))
            self.openEvent.succeed()
            yield self.env.timeout(BoardingGate.OpenInterval)
            self.openEvent = self.env.event()
            self.timeStart = self.env.now + BoardingGate.BreakInterval

    # In Passenger's process
    def serve(self, passenger):
        yield self.openEvent
        self.onPassengerArrive(passenger)
        with self.staffs.request() as req:
            yield req
            mu = self.getServingTime()
            # print(f"Checkpoint has random service time {mu} and mean of service time: {self.serviceTime}")
            yield self.env.timeout(mu) 
        self.onPassengerLeave(passenger) 
    
    def onPassengerLeave(self, passenger):
        # Record data
        dest = passenger.getDestination()
        if dest == Destination.BOARDING:
            print(f"Passenger has id [{passenger.id}] has left boarding gate [{self.gateId}] | Business class: [{self.isFirstClass()}] ! At: {self.env.now}")