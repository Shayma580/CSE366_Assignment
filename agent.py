import pygame
import heapq
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
        self.path = []
        self.moving = False
        self.task_completed = 0
        self.completed_tasks = []
        self.algorithm_name = "A*"
        self.explored_path = []
        self.total_path_cost = 0

    def move(self):
        """Move the agent along the path."""
        if self.path:
            self.position = list(self.path.pop(0))
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.total_path_cost += 1
            self.explored_path.append(self.position)
            self.check_task_completion()

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        pos = tuple(self.position)
        if pos in self.environment.task_locations:
            self.environment.task_locations.pop(pos)
            self.task_completed += 1
            self.find_nearest_task()

    def find_nearest_task(self):
        """Find the nearest task using A* search."""
        tasks = list(self.environment.task_locations.keys())
        paths = [self.find_path_to(t) for t in tasks if self.find_path_to(t)]
        if paths:

            self.path = min(paths, key=len)[1:]
            self.moving = bool(self.path)

    def find_path_to(self, goal):
        """Find a path to the target position using A*."""
        start = tuple(self.position)
        
        open_set = []
        heapq.heappush(open_set, (self.heuristic(start, goal), 0, start))

        closed_set = set()

        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                self.total_path_cost += g_score[current]  # Update total path cost
                return path
            
            closed_set.add(current)
            
            for neighbor in self.get_neighbors(*current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = current_g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

        return []

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from the start to the goal."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def heuristic(self, node, goal):
        """Manhattan distance heuristic."""
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def get_neighbors(self, x, y):
        """Get walkable neighboring positions."""
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def draw_path(self, screen):
        """Visualize the path found by A*."""
        for pos in self.path:

            pygame.draw.rect(screen, (255, 0, 0), (pos[0] * self.grid_size, pos[1] * self.grid_size, self.grid_size, self.grid_size))

    def draw_agent(self, screen):
        """Draw the agent on the screen."""
        screen.blit(self.image, self.rect)

    def draw_info(self, screen):
        """Display the algorithm name and cumulative path cost."""
        font = pygame.font.Font(None, 36)

        algorithm_text = font.render(f"Algorithm: {self.algorithm_name}", True, (0, 0, 0))
        screen.blit(algorithm_text, (10, 10))

        cost_text = font.render(f"Total Path Cost: {self.total_path_cost}", True, (0, 0, 0))
        screen.blit(cost_text, (10, 50))


