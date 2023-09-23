import numpy as ny
import matplotlib.pyplot as fig

def calcNetworkReliability(p, ntkGraph):
    
    n = len(ntkGraph)
    totReliability = 0.0
    for i in range(2**n):
        current_state = genStates(n, i)
        connProb = 1.0
        for j in range(n):
            if current_state[j] == 1:
                connProb *= p
            else:
                connProb *= (1-p)
        if isNetworkConnected(current_state, ntkGraph):
            totReliability += connProb
            
    return totReliability

def genStates(n, i):
    states = ny.array([int(x) for x in bin(i)[2:].zfill(n)])
    return states

def isNetworkConnected(state, ntkGraph):
    vrtx = ny.nonzero(state)[0]
    if len(vrtx) == 0:
        return False
    checked = set()
    stack = [vrtx[0]]
    while stack:
        nd = stack.pop()
        if nd not in checked:
            checked.add(nd)
            nghResult = getNeighbors(nd)
            for neighbor in nghResult:
                if state[neighbor] == 1:
                    stack.append(neighbor)
    return len(checked) == len(vrtx)

def getNeighbors(i):
    nbr = []
    for j in range(len(ntkGraph)):
        if ntkGraph[i][j] == 1:
            nbr.append(j)
    return nbr


if __name__ == "__main__":
    
    ntkGraph = [[0, 1, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 0],
                [1, 1, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 1, 1, 0],
                [1, 0, 1, 0, 0, 1, 0, 1],
                [0, 1, 0, 1, 1, 0, 1, 1],
                [1, 0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 0, 1, 1, 1, 0]]

    
    relValues = []
    pValues = [0.05 + i * 0.05 for i in range(0, 20)]
    for p in pValues:
        rel = calcNetworkReliability(p, ntkGraph)
        relValues.append(rel)

    for p, r in zip(pValues, relValues):
        print(f"For Probability p = {p:.2f}, Value of reliability = {r:.4f}")

    fig.plot(pValues, relValues, marker = 'o', color = 'g')
    fig.xlabel('Probability (p)')
    fig.ylabel('Network Reliability')
    fig.title('Network Reliability vs Node up Probability (p)')
    fig.show()
