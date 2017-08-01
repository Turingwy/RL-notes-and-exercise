states = [i for i in range(16)]
values = [0 for _ in range(16)]
actions = ['n', 'e', 's', 'w']
ds_actions = {'n':-4, 'e':1, 's':4, 'w':-1}
discount = 1
policy = []

def initPolicy():
    global policy
    for _ in range(16):
        policy.append({"n":0.25, "e":0.25, "s":0.25, "w":0.25})

def nextState(s, a):

    if (s < 4 and a == 'n') or (s > 11 and a == 's') \
        or (s%4 == 0 and a == 'w') or ((s+1)%4==0 and a == 'e'):
        return s

    return s+ds_actions[a]

def isTerminator(s):
    return s in [0, 15]

def oneIteration():
    for s in range(16):
        if isTerminator(s):
            continue
        v = 0
        for a in actions:
            nextS = nextState(s, a)
            v += policy[s][a]*(-1+values[nextS])

        values[s] = v

def printValue(v):
  for i in range(16):
    print('{0:>6.2f}'.format(v[i]),end = " ")
    if (i+1)%4 == 0:
      print("")
  print()

initPolicy()
for _ in range(200):
    oneIteration()

printValue(values)





