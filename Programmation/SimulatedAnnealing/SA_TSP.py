from typing import List
from math import sqrt, exp
import numpy as np
import random as rn
import matplotlib.pyplot as plt


class Node(object):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return "[x: " + str(self.x) + ", y: " + str(self.y) + "]"


class TSP(object):
    def __init__(self, nodes: List[Node]) -> None:
        self.nodes: List[Node] = nodes
        self.temp = sqrt(len(nodes))
        self.stop_tmp = 1e-8
        self.stop_iteration = 10000
        self.temp_alpha = 0.995
        self.current_cost = float("inf")
        self.current_solution = []
        self.states = []
        self.costs = []
        self.temps = []
    
    def metropolisCriteria(self, new_cost):
        delta = new_cost - self.current_cost
        if delta < 0:
            return True
        if(np.random.random() < exp(-delta / self.temp)):
            return True
        return False
    
    def randomStartClosestNeighbour(self):
        result: List[Node] = []
        current_node = rn.choice(self.nodes)
        result.append(current_node)
        current_array = self.nodes.copy()
        current_array.remove(current_node)
        while(len(current_array) > 0):
            next_node = min(current_array, key=lambda x: self.distance(current_node, x))
            current_array.remove(next_node)
            result.append(next_node)

        return result, self.cost(result)

    def anneal(self):
        self.current_solution, self.current_cost = self.randomStartClosestNeighbour()
        self.states.append(self.current_solution)
        self.costs.append(self.current_cost)

        i = 0
        while self.temp >= self.stop_tmp and i < self.stop_iteration:
            candidate = self.current_solution.copy()
            # Generate a neighbour state: swap 2 nodes
            node0 = rn.randint(0, len(candidate)-1)
            node1 = rn.randint(0, len(candidate)-1)
            candidate[node0], candidate[node1] = candidate[node1], candidate[node0]
            new_cost = self.cost(candidate)

            if(self.metropolisCriteria(new_cost)):
                self.current_solution, self.current_cost = candidate, new_cost
                self.states.append(self.current_solution)
                self.costs.append(self.current_cost)
            self.temps.append(self.temp)
            self.temp *= self.temp_alpha
            i += 1
        print(str(i) + " iterations; final temp: " + str(self.temp))
        
        return self.current_solution, self.current_cost
    
    def cost(self, solution: List[Node]):
        total_distance: float = 0
        for i in range(0, len(solution)):
            total_distance += self.distance(solution[i], solution[(i+1) % len(solution)])
        return total_distance

    def distance(self, node1: int, node2: int):
        node_1 = self.nodes[node1]
        node_2 = self.nodes[node2]
        return sqrt((node_1.x - node_2.x)**2 + (node_1.y - node_2.y)**2)
    
    def distance(self, node1: Node, node2: Node):
        return sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    
    def plot(self):
        x, y = self.splitAxis(self.current_solution)
        plt.scatter(x, y, c='black')
        plt.plot(x, y)
        plt.show()
    
    def splitAxis(self, solution: List[Node]):
        x = []
        y = []
        for i in solution:
            x.append(i.x)
            y.append(i.y)
        x.append(solution[0].x)
        y.append(solution[0].y)
        return x, y


# Generate a random list of points
nb_nodes = 10
list: List[Node] = []
for i in range(nb_nodes):
    new_node = Node(rn.randrange(-10, 10), rn.randrange(-10, 10))
    list.append(new_node)

# Solve the problem
my_tsp = TSP(list)
solution, cost = my_tsp.anneal()

# Draw the evolution of solutions
fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(0, len(my_tsp.states)):
    x, y = my_tsp.splitAxis(my_tsp.states[i])
    ax.clear()
    ax.title.set_text('Cost: ' + str(my_tsp.costs[i]) + ' ; Temperature: ' + str(my_tsp.temps[i]))
    ax.scatter(x, y, c='black')
    ax.plot(x, y)

    plt.pause(0.001)


