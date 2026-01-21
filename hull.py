from datasets import DataSet
import matplotlib.pyplot as plt
import random as rd

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

    def medianIndexAux(self,List, k): #fonction qui trouve le k-ème plus petit élément dans une liste
        if len(List)<=4:
            List = List.sort()
            return List[k]
        n = len(List)
        q = n//5
        Lsepare = [[List[5*i+j] for j in range(5)] for i in range(q)]
        for i in range(q):
            Lsepare[i]=Lsepare[i].sort()
        pivot = self.medianIndexAux([Lsepare[i][2] for i in range(q)],q//2)
        Lpivot1 = []
        Lpivot2 = []
        for x in List :
            if x <= pivot :
                Lpivot1.append(x)
            else :
                Lpivot2.append(x)
        if len(Lpivot1)>=k :
            return self.medianIndexAux(Lpivot1,k)
        else :
            return self.medianIndexAux(Lpivot2,k-len(Lpivot1))

    def medianIndex(List):
        return List.medianIndexAux(len(List)//2)

    def oneSide(List,x):
        n = len(List)
        if List[0][0] < x: #on trouve deux indices i et j tels que x_i < x < x_j
            i = 0
            j = 1
            while j < n and List[j][0] < x : #par hypothèse sur x, on trouvera forcément j vérifiant x < x_j
                j+=1
        if List[0][0] > x:
            j = 0
            i = 1
            while i < n and List[i][0] > x :
                i+=1
        ordre = []
        for k in range(n):
            if k!=i and k!=j:
                ordre.append(k)
        ordre = rd.shuffle(ordre) #on tire l'ordre dans lequel on va ajouter nos points.
        baseg = List[i]
        based = List[j]
        for k in ordre:
            if List[k][1] > (based[1]-baseg[1])/(based[0]-baseg[0])*(List[k][0]-baseg[0])+baseg[1]:
                if List[k][0] > x:
                    based = List[k]
                else :
                    baseg = List[k]
        return (baseg,based)
    
    Reponse = []

    def upperhull(List): 
        n = len(List)
        if n <= 1 :
            break
        index = medianIndex([List[k][0] for k in range(n)])
        indexbis = medianIndexAux([List[k][0],len(List)//2+1])
        x = (List[index][0]+List[indexbis][0])/2 #on s'assure de trouver un x différent des x_i
        baseg,based = oneSide(List,x)
        Reponse.append((baseg,based))
        Listg = []
        Listd = []
        for y in List:
            if y[0]<baseg[0]:
                Listg.append(y)
            else : 
                Listd.append(y)
        upperhull(Listg)
        upperhull(Listd)
        break


    def osWrap(self):
        pass

    

if __name__ == '__main__' :
    dataset = DataSet(size=101, method='A', seed=42)
    hull = SweepingHull(dataset)

    hull.visualize()