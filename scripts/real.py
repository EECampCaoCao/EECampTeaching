from simulator import Simulator
from drone import RealDrone, SimpleVirtualDrone
from controller import (ConConController, 
                        SingleAxisController)
# from controller import ConConController

def main():
    drone = RealDrone()
    # controller = ConConController(drone=drone,
            # log=True)
    controller = SingleAxisController(drone=drone, log=True)
    sim = Simulator(drone=drone, controller=controller)
    sim.start()

