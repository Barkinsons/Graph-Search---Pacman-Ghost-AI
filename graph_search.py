from graph import Node

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