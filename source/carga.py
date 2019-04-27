
class CargaRotativa:
    
    def __init__(self, I=1):
        self.I = I #momento de inércia
        self.T = 0
        self.f_torque = None
    
    def get_torque(self, w):
        if callable(self.f_torque):
            return self.f_torque(w)
        else:
            return 0
    
    def get_rpm(self, T, to, t, wo, limite):
        if t == 0: return 0
        Tr = self.get_torque(wo)
        #if Tr < T: T = T - Tr; else: T = 
        a = (T - Tr) / self.I
        w = wo + a * (t - to)
        if w > limite: return limite
        return w
    
    def set_torque(self, T):
        self.T = T
