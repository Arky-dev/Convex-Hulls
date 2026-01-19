import random as rd
from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt

class DataSet :

    def __init__(self, size: int = 100, method: str = 'B', seed=-1):

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
            case _:
                raise NameError('Given type is not in [A, B, C, D]')
        
        self.x_list = [elem[0] for elem in self.dataset]
        self.y_list = [elem[1] for elem in self.dataset]

    def __len__(self):
        return self.size
        
    def genA(self):
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
        
        return rotated_points

    def genB(self, points=-1):
        if points != -1:
            return [(rd.random(), rd.random()) for _ in range(points)]
        return [(rd.random(), rd.random()) for _ in range(self.size)]

    def genC(self):
        points = []
        for _ in range(self.size):
            r2, theta = rd.random(), 2*pi*rd.random()
            x,y = sqrt(r2)*cos(theta)/2+0.5, sqrt(r2)*sin(theta)/2+0.5
            points.append((x,y))

        return points

    def genD(self):
        points = []
        for _ in range(self.size):
            theta = 2*pi*rd.random()
            x,y = cos(theta)/2+0.5, sin(theta)/2+0.5
            points.append((x,y))

        return points


    def sort(self, key):
        self.dataset = sorted(self.dataset, key=key)

        self.x_list = [elem[0] for elem in self.dataset]
        self.y_list = [elem[1] for elem in self.dataset]


    def visualize(self):
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

    DS = DataSet(size = 100, method='C', seed=42)
    print(len(DS))
    DS.visualize()
    