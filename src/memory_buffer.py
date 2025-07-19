# memory_buffer.py

from collections import deque

class MemoryBuffer:
    def __init__(self, maxlen=5):
        self.gamma_buffer = deque(maxlen=maxlen)
        self.rho_buffer = deque(maxlen=maxlen)

    def update(self, gamma, rho):
        self.gamma_buffer.append(gamma)
        self.rho_buffer.append(rho)

    def get_smoothed(self):
        if len(self.gamma_buffer) == 0 or len(self.rho_buffer) == 0:
            return 0.0, 0.0
        smoothed_gamma = sum(self.gamma_buffer) / len(self.gamma_buffer)
        smoothed_rho = sum(self.rho_buffer) / len(self.rho_buffer)
        return smoothed_gamma, smoothed_rho
