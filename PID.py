

class PID:
    def __init__(self, kP : float, kI : float, kD : float):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.target = 0
        self.prevError = 0
        self.integral = 0
    
    def reset(self):
        self.prevError = 0
        self.integral = 0

    def setTarget(self, target : float):
        self.target = target

    def step(self, input : float, dt : float):
        error = self.target - input
        derivative = (error - self.prevError) / dt
        self.integral += error * dt
        self.prevError = error

        return error * self.kP + self.integral * self.kI + derivative * self.kD

    