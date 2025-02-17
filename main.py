from PIL import Image, ImageDraw
from usage import Node, Frontier

class Greedy:
    def __init__(self, filename):
        with open(filename) as f:
            data =  f.read()
        if data.count("A") != 1 or data.count("B") != 1:
            raise Exception("Not Worth it")
        self.data = data.splitlines()
        self.heuristicData = []
        self.height = len(self.data)
        self.width = max(len(i) for i in self.data)
        self.start, self.goal = None, None
        self.walls = []
        self.solution = None
        self.numExplored = 0
        self.visited = set()
        self.getWalls()
        self.heuristicFunction()

    def getWalls(self):
        for i in range(self.height):
            x = []
            try:
                for j in range(self.width):
                    if self.data[i][j] == "A":
                        self.start = (i, j)
                        x.append(False)
                    elif self.data[i][j] == 'B':
                        self.goal = (i, j)
                        x.append(False)
                    elif self.data[i][j] == " ":
                        x.append(False)
                    else:
                        x.append(True)
            except IndexError:
                x.append(False)
            self.walls.append(x)


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                elif not self.walls[i][j]:
                    print(" ", end="")
                else:
                    print("█", end="")
            print()

    def neighbour(self, state):

        r, c = state
        actions = (
            ("up", (r-1, c)),
            ("down", (r+1, c)),
            ("left", (r, c-1)),
            ("right", (r, c+1)),
        )
        result = []
        for action, (i, j) in actions:
            if 0 <= i < self.height and 0 <= j < self.width and not self.walls[i][j] and (i, j) not in self.visited:
                result.append((self.heuristicData[i][j], (i, j)))
        result.sort()
        return result

    def heuristicFunction(self):
        """
        Assign Heuristic value to points in maze
        """
        x, y = self.goal
        for i in range(self.height):
            r = []
            try:
                for j in range(self.width):
                    if not self.walls[i][j] and (i, j) is not self.goal and (i, j) is not self.start:
                        a, b = x-i, y-j
                        a = a*-1 if a < 0 else a
                        b = b*-1 if b < 0 else b
                        ans = a+b
                        r.append(ans)
                    else:
                        r.append(float("inf"))
                self.heuristicData.append((r))
            except IndexError:
                pass

    def printHeuristic(self):
        """        Print complete mmaze with heuristic values attached to each point """
        for i in range(self.height):
            try:
                for j in range(self.width):
                    if self.walls[i][j]:
                        print("█", end="")
                    elif  (i, j) == self.start:
                        print("A", end="")
                    elif (i, j) == self.goal:
                        print("B", end="")
                    else:
                        print(self.heuristicData[i][j], end="")
                print()
            except IndexError:
                pass

    def solve(self):
        front = Frontier()
        node = Node(state=self.start)
        front.add(node)
        while True:
            if front.isEmpty():
                raise Exception("No solution")

            node = front.getNode()
            if node.state == self.goal:
                heuristic = []
                cells = []
                while node.parent is not None:
                    heuristic.append(node.dis)
                    cells.append(node.state)
                    node = node.parent

                heuristic.reverse()
                cells.reverse()
                self.solution = [heuristic, cells]
                return
            self.numExplored += 1
            self.visited.add(node.state)
            for dis, (i, j) in self.neighbour(node.state):
                child = Node(state=(i, j), dis=dis, parent=node)
                front.add(child)


    def outImage(self, filename, show_explored=False):
        size = 50
        border = 2
        img = Image.new("RGBA", (size*self.height, size*self.width), "black")
        draw = ImageDraw.Draw(img)
        solution = self.solution[1] if self.solution is not None else None
        for i, r in enumerate(self.walls):
            for j, col in enumerate(r):
                if (i, j) == self.goal:
                    fill = (0, 255, 0)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif solution is not None and (i, j) in solution:
                    fill = (100, 100, 100)
                elif show_explored and (i, j) in self.visited:
                    fill = (0 ,255, 255)
                elif not self.walls[i][j]:
                    fill = (240, 240, 240)
                else:
                    fill = (30, 30, 30)
                draw.rectangle(
                    ([(j*size + border, i*size + border), ((j+1)*size - border, (i+1)*size - border)]), fill=fill)
        img.save(filename)



filename = 'maze2'
m = Greedy(filename + '.txt')
m.print()
print("\n\n\n Heuristic \n\n\n")

m.printHeuristic()

print("\n\n\n Solving \n\n\n")
m.solve()

m.print()
print(m.numExplored)

m.outImage(filename+".png", True)
