from datasets import DataSet
import matplotlib.pyplot as plt
import random as rd
import copy

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



class OSHull(Hull) :

    def __init__(self, dataset):
        super().__init__(dataset)
        self.osWrap()

    def medianAux(self, List, k): #fonction qui trouve le k-ème plus petit élément dans une liste
        if len(List)<=4:
            List.sort()
            return List[k-1]
        n = len(List)
        q = n//5
        Lsepare = [[List[5*i+j] for j in range(5)] for i in range(q)]
        for i in range(q):
            Lsepare[i].sort()
        pivot = self.medianAux([Lsepare[i][2] for i in range(q)],q//2)
        Lpivot1 = [x for x in List if x<=pivot]
        Lpivot2 = [x for x in List if x>pivot]
        
        if len(Lpivot1)>=k :
            return self.medianAux(Lpivot1,k)
        else :
            return self.medianAux(Lpivot2,k-len(Lpivot1))

    def median(self, List):
        return self.medianAux(List,len(List)//2)

    def oneSide(self, List, x):
        n = len(List)
        
        left_points = [p for p in List if p[0] < x]
        right_points = [p for p in List if p[0] > x]
        
        baseg = max(left_points, key=lambda p: p[1])
        based = max(right_points, key=lambda p: p[1])

        ordre = [k for k in range(n) if List[k][2] != baseg[2] and List[k][2] != based[2]]
        rd.shuffle(ordre) #on tire l'ordre dans lequel on va ajouter nos points.

        for k in ordre:
            if List[k][1] > (based[1]-baseg[1])/(based[0]-baseg[0])*(List[k][0]-baseg[0])+baseg[1]:
                if List[k][0] > x:
                    based = List[k]
                else :
                    baseg = List[k]
        return (baseg,based)


    def upperhull(self, List): 
        n = len(List)
        if n == 0:
            return []
        if n == 1 :
            return [List[0][2]]
        if n == 2:
            if List[0][0] < List[1][0]:
                return [List[0][2], List[1][2]]
            else:
                return [List[1][2], List[0][2]]
        med = self.median([List[k][0] for k in range(n)])
        medbis = self.medianAux([List[k][0] for k in range(n)],len(List)//2+1)
        x = (med+medbis)/2 #on s'assure de trouver un x différent des x_i
        baseg, based = self.oneSide(List,x)
        Listg = [y for y in List if y[0] < baseg[0]]
        Listg.append(baseg)
        
        Listd = [y for y in List if y[0] > based[0]]
        Listd.insert(0, based)

        return self.upperhull(Listg)+self.upperhull(Listd)


    def osWrap(self):
        self.upper = True
        indexed_data = [(p[0], p[1], i) for i, p in enumerate(self.dataset.dataset)]
        upper_indexes = self.upperhull(indexed_data)

        Listcopie = [(p[0], -p[1], p[2]) for p in indexed_data]
        self.upper = False
        lower_indexes = self.upperhull(Listcopie)

        self.hull = upper_indexes + lower_indexes[::-1][1:-1]
        print(self.hull)
        return


if __name__ == '__main__' :
    dataset = DataSet(size=101, method='B', seed=40)
    hull = OSHull(dataset)

    hull.visualize()