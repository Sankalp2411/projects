class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = 0
        self.y = 0

    def follow(self, target_x: int, target_y: int, tile_size: int):
        self.x = target_x * tile_size - self.screen_width // 2
        self.y = target_y * tile_size - self.screen_height // 2

    def apply(self, world_x: int, world_y: int):
        return world_x - self.x, world_y - self.y
