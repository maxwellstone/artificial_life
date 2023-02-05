class Part:
    def __init__(self, name: str, pos: list[float], size: list[float], sensor: bool):
        self.name = name
        self.pos = pos
        self.size = size
        self.sensor = sensor