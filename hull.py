from datasets import DataSet
import matplotlib.pyplot as plt


class Hull :

    def __init__(self, dataset):
        self.dataset = dataset
        self.hull = []


    def orient(self,i,j,k):
        x1, y1 = self.dataset.x_list[i], self.dataset.y_list[i]
        x2, y2 = self.dataset.x_list[j], self.dataset.y_list[j]
        x3, y3 = self.dataset.x_list[k], self.dataset.y_list[k]

        d = (x2-x1) * (y3-y1) - (y2-y1) * (x3-x1)
        if d > 0: 
            return 1
        elif d < 0:
            return -1
        return 0
    

    def visualize(self):
        hull = self.hull
        hull.append(hull[0])

        print(hull)

        plt.figure(figsize=(6, 6))
        plt.scatter(self.dataset.x_list, self.dataset.y_list, s=10, alpha=0.6)
        plt.title(f"Hull of {self.dataset.size} points according to distribution method {self.dataset.method}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.grid(True, linestyle='--', alpha=0.5)

        plt.plot([self.dataset.x_list[i] for i in hull], [self.dataset.y_list[i] for i in hull], 'ro', [self.dataset.x_list[i] for i in hull], [self.dataset.y_list[i] for i in hull])
        plt.show()



class SweepingHull(Hull) :

    def __init__(self, dataset):
        super().__init__(dataset)
        self.sweep()
    
    def updateUpperHull(self, pivot):
        while len(self.upperHull) >=2 and self.orient(self.upperHull[-2], self.upperHull[-1], pivot+1) != -1:
            self.upperHull.pop()
        self.upperHull.append(pivot+1)

    def updateLowerHull(self, pivot):
        while len(self.lowerHull) >=2 and self.orient(self.lowerHull[-2], self.lowerHull[-1], pivot+1) != 1:
            self.lowerHull.pop()
        self.lowerHull.append(pivot+1)
    
    def combineHulls(self):
        self.hull = list(self.lowerHull)
        for elem in self.upperHull[::-1][1:-1]:
            self.hull.append(elem)

    def sweep(self):
        self.dataset.sort(key=lambda x : (x[1], x[0]))

        self.upperHull = [0, 1]
        self.lowerHull = [0, 1]
        for i in range(1, len(self.dataset)-1):
            self.updateUpperHull(i)
            self.updateLowerHull(i)
        
        self.combineHulls()



class GiftWrappingHull(Hull) :

    def __init__(self, dataset):
        super().__init__(dataset)
        self.giftWrap()



class OSHull :

    def __init__(self, dataset):
        super().__init__(dataset)
        self.osWrap()

    def medianIndex(self):
        pass

    def osWrap(self):
        pass

    

if __name__ == '__main__' :
    dataset = DataSet(size=101, method='A', seed=42)
    hull = SweepingHull(dataset)

    hull.visualize()