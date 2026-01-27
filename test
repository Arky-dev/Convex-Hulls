import random as rd

def medianIndexAux(List, k): #fonction qui trouve le k-ème plus petit élément dans une liste
    if len(List)<=4:
        List.sort()
        return List[k-1]
    n = len(List)
    q = n//5
    Lsepare = [[List[5*i+j] for j in range(5)] for i in range(q)]
    for i in range(q):
        Lsepare[i].sort()
    pivot = medianIndexAux([Lsepare[i][2] for i in range(q)],q//2)
    Lpivot1 = []
    Lpivot2 = []
    for x in List :
        if x <= pivot :
            Lpivot1.append(x)
        else :
            Lpivot2.append(x)
    if len(Lpivot1)>=k :
        return medianIndexAux(Lpivot1,k)
    else :
        return medianIndexAux(Lpivot2,k-len(Lpivot1))

def medianIndex(List):
    return medianIndexAux(List,len(List)//2)


if __name__ == '__main__' : 
    print(medianIndex([1,9,4,6,2,3,5,8,7,10,11,15,14,13,12,16]))

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
    print(ordre)
    rd.shuffle(ordre) #on tire l'ordre dans lequel on va ajouter nos points.
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
        return 
    index = medianIndex([List[k][0] for k in range(n)])
    indexbis = medianIndexAux([List[k][0] for k in range(n)],len(List)//2+1)
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
    return 

if __name__ == '__main__' : 
    print(upperhull([[1,0],[0,1]]))
    print(Reponse)

