class Cell:
    def __init__(self, x, y):
        self.neighbours = []
        self.walls = {
            "south": True,
            "north": True,
            "east": True,
            "west": True
        }
        self.visited = False
        self.reserved = False
        self.path = False
        self.x = x
        self.y = y


    def destroy_wall(self, direction):
        self.walls[direction] = False

    def add_neighbour(self, cell: 'Cell'):
        self.neighbours.append(cell)

    def count_wall(self):
        return len([v for v in self.walls.values() if v])

    def is_wall_between(self, n):
        if n.x == self.x - 1:
            return self.walls['west']
        elif n.x == self.x + 1: 
            return self.walls['east']
        elif n.y == self.y - 1:
            return self.walls['north']
        elif n.y == self.y + 1:
            return self.walls['south']
