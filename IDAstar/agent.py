import pygame
from collections import deque

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []
        self.moving = False
        self.explored_path = []

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.explored_path.append(self.position)
            self.check_task_completion()
        else:
            self.moving = False

    def check_task_completion(self):

        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def heuristic(self, start, goal):

        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def ida_star(self, start, goal):

        def dfs(path, g, limit):
            current = path[-1]
            if current == goal:
                return path
            if g + self.heuristic(current, goal) > limit:
                return None
            for neighbor in self.get_neighbors(*current):
                if neighbor not in path:
                    new_path = path + [neighbor]
                    result = dfs(new_path, g + 1, limit)
                    if result:
                        return result
            return None

        limit = self.heuristic(start, goal)
        while True:
            path = dfs([start], 0, limit)
            if path:
                return path
            limit += 1

    def find_nearest_task(self):

        nearest_task = None
        shortest_path = None
        for task_position in self.environment.task_locations.keys():
            path = self.ida_star(tuple(self.position), task_position)
            if path and (not shortest_path or len(path) < len(shortest_path)):
                shortest_path = path
                nearest_task = task_position
        if shortest_path:
            self.path = shortest_path[1:]
            self.moving = True

    def get_neighbors(self, x, y):

        neighbors = []
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
        for _, (dx, dy) in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors




