from typing import List
from math import sqrt, exp
import numpy as np
import random as rn
import matplotlib.pyplot as plt
import time

class Node(object):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def distance(self, other) -> float:
        # print("dist 2d")
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self) -> str:
        return "[x: " + str(self.x) + ", y: " + str(self.y) + "]"

class Node3D(Node):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y)
        self.z = z

    def distance(self, other) -> float:
        # print("dist 3d")
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + + (self.z - other.z)**2)
    
    def __str__(self) -> str:
        return "[x: " + str(self.x) + ", y: " + str(self.y) + + ", z: " + str(self.z) +  "]"

class TSP(object):
    '''
        Handles the Travelling Salesman Problem using Simulated Annealing
    '''
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
    
    def metropolisCriterion(self, new_cost) -> bool:
        ''' Checks the validity of a new cost, using Metropolis acceptance criterion '''
        delta = new_cost - self.current_cost
        if delta < 0:
            return True
        if(np.random.random() < exp(-delta / self.temp)):
            return True
        return False
    
    def randomStartClosestNeighbour(self):
        ''' Chooses a random starting configuration, using the closest neighbour method '''
        result: List[Node] = []
        current_node = rn.choice(self.nodes) # Choose a random starting node
        result.append(current_node)
        current_array = self.nodes.copy()
        current_array.remove(current_node)
        while(len(current_array) > 0):
            next_node = min(current_array, key=lambda x: self.distance(current_node, x)) # Get the closest node from the previous one
            current_array.remove(next_node)
            result.append(next_node)

        return result, self.cost(result)

    def anneal(self):
        ''' Computes the optimal solution using the Simulated Annealing algorithm '''

        # Setup the initial configuration
        self.current_solution, self.current_cost = self.randomStartClosestNeighbour()
        self.states.append(self.current_solution)
        self.costs.append(self.current_cost)
        self.temps.append(self.temp)

        i = 0
        last_equal_amount = 0
        while self.temp >= self.stop_tmp and i < self.stop_iteration:
            candidate = self.current_solution.copy()
            # Generate a neighbour state: swap 2 nodes
            node0 = rn.randint(0, len(candidate)-1)
            node1 = rn.randint(0, len(candidate)-1)
            candidate[node0], candidate[node1] = candidate[node1], candidate[node0]
            # Compute cost of new configuration
            new_cost = self.cost(candidate)
            # Check validity of new configuration
            if(self.metropolisCriterion(new_cost)):
                # Handle stop by convergence of solution
                if(new_cost - self.current_cost < 1e-5): last_equal_amount+=1
                else: last_equal_amount = 0
                # Change current configuration
                self.current_solution, self.current_cost = candidate, new_cost
                self.states.append(self.current_solution)
                self.costs.append(self.current_cost)
                self.temps.append(self.temp)

            # Stop optimization if we have converged
            # TODO: check what number should be put here ?
            if(last_equal_amount > 50):
                break
            # Reduce temperature
            self.temp *= self.temp_alpha
            i += 1
        print(str(i) + " iterations; final temp: " + str(self.temp))
        
        return self.current_solution, self.current_cost
    
    def cost(self, solution: List[Node]) -> float:
        ''' Computes the cost of the given solution. The cost is defined as the total length of the closed path '''
        total_distance: float = 0
        for i in range(0, len(solution)):
            total_distance += self.distance(solution[i], solution[(i+1) % len(solution)])
        return total_distance

    def distance(self, node1: int, node2: int) -> float:
        node_1 = self.nodes[node1]
        node_2 = self.nodes[node2]
        return node_1.distance(node_2)
    
    def distance(self, node1: Node, node2: Node) -> float:
        return node1.distance(node2)
    
    def splitAxis(self, solution: List[Node]):
        ''' Splits the array of solutions into 2 (or 3) separate [x], [y] ([z]) vectors (drawing purposes) '''
        x = []
        y = []
        if type(solution[0]) == Node3D:
            z = []
        for i in solution:
            x.append(i.x)
            y.append(i.y)
            if type(solution[0]) == Node3D:
                z.append(i.z)
        x.append(solution[0].x)
        y.append(solution[0].y)
        if type(solution[0]) == Node3D:
            z.append(solution[0].z)
            return x, y, z
        return x, y


def simulate(type: str, nb_nodes: int, range_start: float, range_stop: float) -> None:
    ''' Simulates a run of optimization '''
    list: List[Node] = []
    fig = plt.figure()
    if(type == '2d'):
        ax = fig.add_subplot(111)
        for i in range(0, nb_nodes):
            new_node = Node(rn.randrange(range_start, range_stop), rn.randrange(range_start, range_stop))
            list.append(new_node)
        my_tsp = TSP(list)
        start = time.time()
        my_tsp.anneal()
        delta = time.time() - start
        print("anneal took " + "{:.4f}".format(delta) + " seconds")
        for i in range(0, len(my_tsp.states)):
            x, y = my_tsp.splitAxis(my_tsp.states[i])
            ax.clear()
            ax.title.set_text('Cost: ' + str(my_tsp.costs[i]) + ' ; Temperature: ' + str(my_tsp.temps[i]) + "; Iteration " + str(i+1) + "/" + str(len(my_tsp.states)))
            ax.scatter(x, y, c='black')
            ax.plot(x, y)
            plt.pause(0.0001)
    elif(type == '3d'):
        for i in range(0, nb_nodes):
            new_node = Node3D(rn.randrange(range_start, range_stop), rn.randrange(range_start, range_stop), rn.randrange(range_start, range_stop))
            list.append(new_node)
        ax = fig.add_subplot(111, projection='3d')
        my_tsp = TSP(list)
        start = time.time()
        my_tsp.anneal()
        delta = time.time() - start
        print("anneal took " + "{:.4f}".format(delta) + " seconds")
        for i in range(0, len(my_tsp.states)):
            x, y, z = my_tsp.splitAxis(my_tsp.states[i])
            ax.clear()
            ax.title.set_text('Cost: ' + str(my_tsp.costs[i]) + ' ; Temperature: ' + str(my_tsp.temps[i]) + "; Iteration " + str(i+1) + "/" + str(len(my_tsp.states)))
            ax.scatter(x, y, z, c='black')
            ax.plot(x, y, z)
            plt.pause(0.001)
    else:
        print("Unkown type, must be '2d' or '3d'")
    plt.pause(5)

# Single pass of simulation
simulate('3d', 50, -30, 30)

# Multiple passes: histogram of best solution
nb_passes = 1000
nb_nodes = 40
range_start = -100
range_stop = 100
list: List[Node] = []
for i in range(0, nb_nodes):
    new_node = Node3D(rn.randrange(range_start, range_stop), rn.randrange(range_start, range_stop), rn.randrange(range_start, range_stop))
    list.append(new_node)
costs: List[float] = []
for i in range(0, nb_passes):
    print("iteration " + str(i))
    my_tsp = TSP(list)
    solution, cost = my_tsp.anneal()
    costs.append(cost)

n, bins, patches = plt.hist(x=costs)
plt.grid(axis='y')
plt.xlabel('Final energy')
plt.ylabel('amount')
plt.show()
