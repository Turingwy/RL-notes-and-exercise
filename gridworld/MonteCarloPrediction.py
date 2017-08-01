states = [i for i in range(16)]
error = 0.1
values = [0 for _ in range(16)]
valueCount = [0 for _ in range(16)]
actions = ['n', 'e', 's', 'w']
episodeStates = []
ds_actions = {'n':-4, 'e':1, 's':4, 'w':-1}
discount = 1
policy = []

def nextState(s, a):

    if (s < 4 and a == 'n') or (s > 11 and a == 's') \
        or (s%4 == 0 and a == 'w') or ((s+1)%4==0 and a == 'e'):
        return s

    return s+ds_actions[a]

def isTerminator(s):
    return s in [0, 15]

def printValue(v):
  for i in range(16):
    print('{0:>6.2f}'.format(v[i]),end = " ")
    if (i+1)%4 == 0:
      print("")

def nextAction():
    from random import random
    num = random()
    return actions[int(num/0.25)]

def oneEpisode():
    s = 9
    a = nextAction()
    episodeStates.append(s)
    nextS = nextState(s, a)
    while not isTerminator(nextS):
        episodeStates.append(nextS)
        s = nextS
        a = nextAction()
        nextS = nextState(s, a)


def valueEvaluate():
    global episodeStates
    global error
    error = 0
    for i in range(len(episodeStates)):
        s = episodeStates[i]
        valueCount[s]+=1
        oldValue = values[s]
        values[s] = values[s] + (1/valueCount[s])*(i - len(episodeStates) - values[s])
        if abs(oldValue-values[s]) > error:
            error = abs(oldValue-values[s])
    episodeStates = []

while error > 0.0001:
    oneEpisode()
    valueEvaluate()
    print(error)
printValue(values)
