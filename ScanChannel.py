class ScanChannel:
    def __init__(self, name: str, isEnabled: bool):
        self.name = name
        self.isEnabled = isEnabled
        self.scanPoints = []
