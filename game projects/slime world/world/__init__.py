class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zones = []

        self._generate_fixed_world()

        self.slime = Slime(start_x=5, start_y=5)
