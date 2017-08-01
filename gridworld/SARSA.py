states = [i for i in range(16)]
error = 10
Q = [{'n':0, 'e':0, 's':0, 'w':0} for _ in range(16)]
actions = ['n', 'e', 's', 'w']
ds_actions = {'n':-4, 'e':1, 's':4, 'w':-1}
epsilon = 0.05
values = [0 for _ in range(16)]
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

def nextAction(s):
    from random import random
    global actions
    num = random()
    if num < 1 - 3*epsilon:
        return maxAction(s)
    else:
        actions.remove(maxAction(s))
        num-=(1-3*epsilon)
        num/=epsilon
        num=int(num)
        retAction = actions[num]
        actions = ["n", "e", "s", "w"]
        return retAction

def maxAction(s):
    maxQ = -10000
    maxA = None
    for a in actions:
        if maxQ < Q[s][a]:
            maxA = a
            maxQ = Q[s][a];

    return maxA

def oneEpisode():
    global error
    s = 9
    a = nextAction(s)
    error = 0
    while not isTerminator(s):
        nextS = nextState(s, a)
        nextA = nextAction(nextS)
        oldQ = Q[s][a]
        Q[s][a] = Q[s][a] + (1/100)*(-1+Q[nextS][nextA]-Q[s][a])
        if abs(oldQ-Q[s][a]) > error:
            error = abs(oldQ-Q[s][a])
        s = nextS
        a = nextA

def valueEvaluate():
    for s in range(16):
        a = maxAction(s)
        values[s] = Q[s][a]

i = 0
while error > 0.00005:
    oneEpisode()
    i+=1
    print(error)

valueEvaluate()
printValue(values)
print(i)
