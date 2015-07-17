from simulator import Simulator
from drone import SimpleVirtualDroneWithNoise
from controller import SimpleController

def main():
    drone = SimpleVirtualDroneWithNoise()
    controller = SimpleController(drone=drone,
            log=True)
    sim = Simulator(drone=drone, controller=controller)
    sim.start()
