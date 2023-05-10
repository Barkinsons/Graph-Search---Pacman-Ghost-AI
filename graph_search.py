from graph import Node
from queue import PriorityQueue

class Graph_Search:
    def get_path(start: Node, target: Node) -> list:
        raise NotImplementedError


class Depth_First_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
      
        visited = set()
        stack = [((start, None), [])]

        while stack:

            top, path = stack.pop()
            visited.add(top[0])

            if top[0] == target:
                return path + [top]
            
            for neighbor in top[0].neighbors:
                if neighbor[0] not in visited:
                    stack.append((neighbor, path + [top]))

        return []
    
class Breadth_First_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:

        visited = set()
        queue = [((start, None), [])]

        while queue:
            front, path = queue[0]
            queue = queue[1:]
            visited.add(front[0])

            if front[0] == target:
                return path + [front]

            for neighbor in front[0].neighbors:
                if neighbor[0] not in visited:
                    queue.append((neighbor, path + [front]))

        return []
    
class Best_First_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
        
        closed = set()
        open = PriorityQueue()
        open.put((0, [(start, None)]))

        while not open.empty():
            _, path = open.get()
            cur = path[-1][0]

            if cur == target:
                return path

            if cur in closed:
                continue

            closed.add(cur)

            for neighbor in cur.neighbors:
                if neighbor[0] not in closed:
                    priority = abs(neighbor[0].x - target.x) + abs(neighbor[0].y - target.y) # Manhattan Distance
                    open.put((priority, path + [neighbor]))

        return []


class Iterative_Deepening_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
        depth_limit = 0
        
        while True:
            visited = set()
            path = Iterative_Deepening_Search.depth_limited_search((start, None), target, depth_limit, visited)
            if path:
                return path
            depth_limit += 1

    def depth_limited_search(cur, target, depth_limit: int, visited) -> list:
        if cur[0] == target:
            return [cur]
        
        if depth_limit <= 0 or cur[0] in visited:
            return None
        
        visited.add(cur[0])

        for neighbor in cur[0].neighbors:
            path = Iterative_Deepening_Search.depth_limited_search(neighbor, target, depth_limit-1, visited)
            
            if path:
                return [cur] + path  
    
        return []
            
class A_Star_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
        open_list = PriorityQueue()
        open_list.put((0, (start, None)))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not open_list.empty():
            _, current = open_list.get()

            if current[0] == target:
                return A_Star_Search.reconstruct_path(came_from, current)

            for neighbor in current[0].neighbors:
                new_cost = cost_so_far[current[0]] + A_Star_Search.distance(current[0], neighbor[0])
                if neighbor[0] not in cost_so_far or new_cost < cost_so_far[neighbor[0]]:
                    cost_so_far[neighbor[0]] = new_cost
                    priority = new_cost + A_Star_Search.heuristic(neighbor[0], target)
                    open_list.put((priority, neighbor))
                    came_from[neighbor[0]] = current

        return []
    
    def heuristic(node, target):
        dx = abs(node.x - target.x)
        dy = abs(node.y - target.y)
        return dx + dy
    
    def distance(node1, node2):
        dx = abs(node1.x - node2.x)
        dy = abs(node1.y - node2.y)
        
        return 1 if dx + dy == 1 else 1.414
    
    def reconstruct_path(came_from, node):
        path = []
        
        while node:
            path.append(node)
            node = came_from[node[0]]
        
        return path[::-1]