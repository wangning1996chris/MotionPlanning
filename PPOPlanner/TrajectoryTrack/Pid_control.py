"""
Pure Pursuit For RL
authors: Wang Ning; Yang Hongyi
Date: 2024-04-014
"""
import time
 
class PID:
 
    def __init__(self, P=0.3, I=0.1, D=0.1, current_time=None):
        self.Kp = P
        self.Ki = I
        self.Kd = D
 
        self.sample_time = 0.02
        self.current_time = current_time
        self.last_time = current_time
 
        self.clear()
 
    def clear(self):
        self.SetPoint = 0.0
 
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
 
 
        self.int_error = 0.0
        self.I_max_modify = 20.0
 
        self.output = 0.0
 
    def update(self, set_value, feedback_value, current_time=None):
        """
        math::
             u(k) = K_pe_k + K_i\sum_{j=0}^ke(j)\Delta t + K_d\frac{e(k) - e(k-1)}{\Delta t}
        """
        error = set_value - feedback_value
 
        self.current_time = current_time
        delta_time = self.current_time - self.last_time
 
        if(delta_time >= self.sample_time):
            self.ITerm += error * delta_time
 
            if(self.ITerm < -self.I_max_modify):
                self.ITerm = -self.I_max_modify
            elif(self.ITerm > self.I_max_modify):
                self.ITerm = self.I_max_modify
 
            self.DTerm = 0.0
 
            if delta_time > 0:
                self.DTerm = (error - self.last_error) / delta_time
 
            self.last_time = self.current_time
            self.last_error = error
        
        self.output = (self.Kp * error) + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
        return self.output

    def set_setpoint(self, set_point):
        self.set_point = set_point

    def set_params(self, Kp=None, Ki=None, Kd=None, sample_time=None):
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd
        if sample_time is not None:
            self.sample_time = sample_time

# Test
if __name__ == '__main__':
    pid = PID()
    pid.set_setpoint(10.0)
    pid.set_params(Kp=1.0, Ki=0.5, Kd=0.2)
    acceleration = pid.update(set_value=2, feedback_value=3, current_time=0.05)