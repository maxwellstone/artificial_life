from part import Part

class Joint:
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    def __init__(self, parent: Part, child: Part, pos: list[float], axis: int):
        self.parent = parent
        self.child = child
        self.pos = pos
        self.axis = axis