class ScanChannel:
    def __init__(self, name: str, gain: float):
        self.name = name
        self.gain = gain
        self.scanPoints = []
