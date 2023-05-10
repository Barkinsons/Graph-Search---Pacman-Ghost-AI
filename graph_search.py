from graph import Node
from queue import PriorityQueue

class Graph_Search:
    def get_path(start: Node, target: Node) -> list:
        raise NotImplementedError


class Depth_First_Search(Graph_Search):
    def get_path(self, start: Node, target: Node) -> list:
      
        visited = set()
        stack = [(start, [])]

        while stack:

            top, path = stack.pop()
            visited.add(top)

            if top == target:
                return path + [top]
            
            for neighbor in top.neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [top]))

        return []
    
class Breadth_First_Search(Graph_Search):
    def get_path(self, start: Node, target: Node) -> list:

        visited = set()
        queue = [(start, [])]

        while queue:
            front, path = queue[0]
            queue = queue[1:]
            visited.add(front)

            if front == target:
                return path + [front]

            for neighbor in front.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [front]))

        return []

class Depth_Limited_Search(Graph_Search):
    
    def get_path(self, start: Node, target: Node) -> list:
        depth_limit = 15
        return self.depth_limited_search(start, target, set(), depth_limit)
    
    def depth_limited_search(self, node, target, obstacles: set, depth_limit: int, visited: set = None) -> list:
        if node == target:
            return [node]
        
        if depth_limit <= 0:
            return None
        
        if visited is None:
            visited = set()
        
        visited.add(node)
        
        for neighbor in node.neighbors:
            child = neighbor
            
            if child in visited or child in obstacles:
                continue
            
            path = self.depth_limited_search(child, target, obstacles, depth_limit - 1, visited)
            
            if path is not None:
                return [node] + path
            
        visited.remove(node)
            
        return []
            
class A_Star_Search(Graph_Search):
    def get_path(self, start: Node, target: Node) -> list:
        open_list = PriorityQueue()
        open_list.put((0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not open_list.empty():
            _, current = open_list.get()

            if current == target:
                return self.reconstruct_path(came_from, current)

            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + self.distance(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, target)
                    open_list.put((priority, neighbor))
                    came_from[neighbor] = current

        return []
    
    def heuristic(self, node, target):
        dx = abs(node.x - target.x)
        dy = abs(node.y - target.y)
        return dx + dy
    
    def distance(self, node1, node2):
        dx = abs(node1.x - node2.x)
        dy = abs(node1.y - node2.y)
        
        return 1 if dx + dy == 1 else 1.414
    
    def reconstruct_path(self, came_from, node):
        path = []
        
        while node:
            path.append(node)
            node = came_from[node]
        
        return path[::-1]