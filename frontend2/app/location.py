def generate_locations():
    home_resurant = location(5, 5, 5)


class location:
    def __init__(self, x=-1, y=-1, z=-1):
        self.x = x
        self.y = y
        self.z = z
        self.home_location = None
        self.a_location = None
        self.b_location = None
        self.c_location = None
