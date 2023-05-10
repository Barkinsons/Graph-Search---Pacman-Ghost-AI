from graph import Node
from queue import PriorityQueue

class Graph_Search:
    def get_path(start: Node, target: Node) -> list:
        raise NotImplementedError


class Depth_First_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
      
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
    def get_path(start: Node, target: Node) -> list:

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
    
class Best_First_Search(Graph_Search):
    def get_path(start: Node, target: Node) -> list:
        
        closed = set()
        open = PriorityQueue()
        open.put((0, [start]))

        while not open.empty():
            _, path = open.get()
            cur = path[-1]

            if cur == target:
                return path

            if cur in closed:
                continue

            closed.add(cur)

            for neighbor in cur.neighbors:
                if neighbor not in closed:
                    priority = abs(neighbor.x - target.x) + abs(neighbor.y - target.y) # Manhattan Distance
                    open.put((priority, path + [neighbor]))

        return []
