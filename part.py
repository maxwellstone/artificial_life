import numpy as np

class Part:
    def __init__(self, name: str, world_pos: list[float], pos: list[float], size: list[float], sensor: bool):
        self.name = name
        self.world_pos = world_pos
        self.pos = pos
        self.size = size
        self.sensor = sensor

    def intersects(self, other: "Part") -> bool:
        pos_a = np.asarray(self.world_pos)
        dim_a = np.asarray(self.size)
        min_a = pos_a - dim_a / 2
        max_a = pos_a + dim_a / 2

        pos_b = np.asarray(other.world_pos)
        dim_b = np.asarray(other.size)
        min_b = pos_b - dim_b / 2
        max_b = pos_b + dim_b / 2

        return not (np.any(max_b < min_a) or np.any(min_b > max_a))