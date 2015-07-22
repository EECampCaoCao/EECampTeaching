from mymath.pid import BasePID
import numpy as np

class MyPID(BasePID):
    def __init__(self, kp, ki, kd, *, imax):
        super().__init__(kp, ki, kd, imax=imax)
        self.last_time = None
        # TODO:
        # Init the variables you need...

    def get_control(self, t, err, derr):
        if self.last_time is None:
            self.last_time = t
            return 0.

        # TODO:
        # What should up be ?
        up = 0. 

        # TODO:
        # What should ud be ?
        ud = 0.

        # TODO:
        # Calculate dt. Remember to update
        # some variables you defined
        dt = 0.
        self.last_time = 0.

        # TODO:
        # Calculate the sum of the error.
        something = 0.

        # TODO:
        # Restrict the sum of the error to be within
        # [-self.int_restriction, self.int_restriction]
        if something > self.int_restriction:
            pass

        # TODO:
        # What should ui be ?
        ui = 0.

        # TODO:
        # Return the sum of up, ud and ui !
        return 0.
