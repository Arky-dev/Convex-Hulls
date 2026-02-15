import random as rd
from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt
import copy

class DataSet :
    """
    This class generates 2D datasets for convex hull algorithm testing.

    The points of the dataset are generated in a [0, 1] x [0, 1] square according to 
    four distributions (A, B, C, D) as outlined in the project requirements.

    An extra option to create a dataset from a list of points is available

    Attributes:
        size (int): Total number of points in the dataset.
        method (str): The distribution method used ('A', 'B', 'C', or 'D').
        dataset (list of tuples): The generated points as [(x1, y1), (x2, y2), ...].
        x_list (list): A flat list of all x-coordinates for easy plotting.
        y_list (list): A flat list of all y-coordinates for easy plotting.

    Methods:
        __len__(): Returns the number of points in the dataset.
        genA(): Generates a rotated square of points including 4 explicit corners.
        genB(points=-1): Generates points uniformly distributed in a square.
        genC(): Generates points uniformly distributed inside a disk.
        genD(): Generates points distributed exactly on a circle's boundary.
        sort(key): Sorts the dataset based on a given key (e.g., x or y coordinates).
        visualize(): Renders a scatter plot of the dataset using matplotlib.
    """

    def __init__(self, size: int = 100, method: str = 'B', seed=-1, list=[]):
        """
        Initializes the DataSet with a specific generation method.

        Args:
            size (int): The number of points to generate. Defaults to 100.
            method (str): The distribution type:
                'A' : Rotated square with corners (tests extreme values)
                'B' : Uniform square distribution
                'C' : Uniform disk distribution
                'D' : Circular boundary distribution
                'list' : Specify the list of points used as a dataset
            seed (int): Optional random seed for reproducibility. Default is no seed.
            list (list) : Optional list of points that can be specified to define a specific dataset
        """

        if seed != -1:
            rd.seed(seed)

        self.size = size
        self.method = method

        match method :
            case 'A':
                self.dataset = self.genA()
            case 'B':
                self.dataset = self.genB()
            case 'C':
                self.dataset = self.genC()
            case 'D':
                self.dataset = self.genD()
            case 'list':
                self.dataset = copy.deepcopy(list)
                self.size = len(self.dataset)
            case _:
                raise NameError('Given type is not in [A, B, C, D]')
        
        self.x_list = [elem[0] for elem in self.dataset]
        self.y_list = [elem[1] for elem in self.dataset]

    def __len__(self):
        return self.size
    
    def __str__(self):
        return str(self.dataset)
        
    def genA(self):
        """
        Generates Dataset A: A set of points with four extreme corners.
        
        The points are generated in a unit square, four corners are added at 
        (0,0), (1,0), (0,1), and (1,1), and then the entire set is rotated by a 
        random angle and scaled to fit back into the [0, 1] unit square. The
        final list is then shuffled.
        """
        default = self.genB(points = self.size - 4)
        default.append((0,0))
        default.append((1,0))
        default.append((0,1))
        default.append((1,1))

        angle = rd.random()*pi*2

        rotated_points = []
        c, s = cos(angle), sin(angle)
        scale_factor = 1 / (abs(c) + abs(s))

        for (x,y) in default:
            x1, y1 = x-0.5, y-0.5
            x2, y2 = c*x1-s*y1, s*x1+c*y1
            x2, y2 = scale_factor*x2+0.5, scale_factor*y2+0.5

            rotated_points.append((x2, y2))
        
        rd.shuffle(rotated_points)
        
        return rotated_points

    def genB(self, points : int = -1):
        """
        Generates Dataset B: Uniform distribution in a square.

        The points are generated uniformly in a unit square with corners (0,0), 
        (1,0), (0,1), and (1,1).

        Args:
            points (int): Number of points to generate. If -1, uses self.size.
        
        Returns:
            list: A list of (x, y) coordinates where x, y are in [0, 1].
        """
        if points != -1:
            return [(rd.random(), rd.random()) for _ in range(points)]
        return [(rd.random(), rd.random()) for _ in range(self.size)]

    def genC(self):
        """
        Generates Dataset C: Uniform distribution in a disk.
        
        The points are generated uniformly in a disk centered at (0.5, 0.5) with 
        radius 0.5, according to : x = sqrt(r) * cos(theta), y = sqrt(r) * sin(theta).
        transformations are applied to the selected radius and angle to ensure the 
        uniform distribution.
        """
        points = []
        for _ in range(self.size):
            r2, theta = rd.random(), 2*pi*rd.random()
            x,y = sqrt(r2)*cos(theta)/2+0.5, sqrt(r2)*sin(theta)/2+0.5
            points.append((x,y))

        return points

    def genD(self):
        """
        Generates Dataset D: Points on the boundary of a circle.
        
        The points are generated such that they lie exactly on the circle centered 
        at (0.5, 0.5) with radius 0.5 according to a random angle selected uniformly.
        """
        points = []
        for _ in range(self.size):
            theta = 2*pi*rd.random()
            x,y = cos(theta)/2+0.5, sin(theta)/2+0.5
            points.append((x,y))

        return points


    def sort(self, key):
        """
        Sorts the dataset in-place and updates coordinate lists.

        Args:
            key (function): The sorting criteria.
        """
        self.dataset = sorted(self.dataset, key=key)

        self.x_list = [elem[0] for elem in self.dataset]
        self.y_list = [elem[1] for elem in self.dataset]


    def visualize(self):
        """
        Displays the dataset using a Matplotlib scatter plot.
        """
        plt.figure(figsize=(6, 6))
        plt.scatter(self.x_list, self.y_list, s=10, alpha=0.6)
        plt.title(f"Distribution of {self.size} points according to method {self.method}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()



if __name__ == '__main__' : 

    DS = DataSet(size = 1000, method='A', seed=42)
    DS.visualize()
    