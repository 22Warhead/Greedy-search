from numpy.testing.print_coercion_tables import print_new_cast_table


class Node:
    def __init__(self, state, action=None, parent=None, dis=float('inf')):
        self.state = state
        self.action = action
        self.parent = parent
        self.dis = dis


class Frontier:
    def __init__(self):
        self.frontier = []

    def isEmpty(self):
        return len(self.frontier) == 0

    def contains(self, state):
        return any(i.state == state for i in self.frontier)

    def getNode(self):
        if self.isEmpty():
            raise Exception("Empty Frontier")
        x = float('inf')
        ans = 0
        for i in range(len(self.frontier)):
            if self.frontier[i].dis < x:
                x = self.frontier[i].dis
                ans = i
        ans = self.frontier.pop(ans)
        return ans

    def add(self, node):
        self.frontier.append(node)


