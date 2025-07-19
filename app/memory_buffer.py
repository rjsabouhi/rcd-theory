# app/memory_buffer.py

class SymbolMemory:
    def __init__(self, maxlen=5):
        self.history = []
        self.maxlen = maxlen

    def add(self, symbol: str, alpha, beta, delta):
        entry = {"symbol": symbol, "alpha": alpha, "beta": beta, "delta": delta}
        self.history.append(entry)
        if len(self.history) > self.maxlen:
            self.history.pop(0)

    def get_recent(self):
        return self.history

    def clear(self):
        self.history = []
