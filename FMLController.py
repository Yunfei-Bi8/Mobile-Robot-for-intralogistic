import time
import numpy as np

class PController:
    def __init__(self, kp, target_value):
        self.kp = kp
        self.target_value = target_value
    
    def get_u(self,current_value):
        error = self.target_value - current_value # Compute error 30 100
        u = self.kp * error # compute u
        return u


class PIController:
    def __init__(self, kp,ki, target_value):
        self.kp = kp
        self.ki = ki
        self.target_value = target_value
        self.last_call= time.time()
        self.dt =0
        self.integral =0
    
    def get_u(self,current_value):
        now = time.time()
        self.dt = now-self.last_call##check point1
        error = self.target_value - current_value # compute error 
        self.integral += error * self.dt # Update integral value
        u = (self.kp * error) + (self.ki * self.integral) # Compute U from P and I portion
        # Update time for next call
        self.last_call = now
        return u