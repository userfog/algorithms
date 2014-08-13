import os
import sys
import pprint
import heapq
from decimal import Decimal
pp = pprint.PrettyPrinter(indent=4)


myInput = []
graph = []

class Queue:
  def __init__(self):
    self.q = []

  def is_empty(self):
    if len(self.q) == 0:
      return True
    return False

  def push(self, vertex, distance, state):
    self.q.insert(0, (vertex, distance, state))

  def pop(self):
    return self.q.pop()

def value(t):
  return graph[t[1]][t[0]]

def adj(t, myInput):
  l = []
  if t[1] - 1 >= 0:
    l.append((t[0], t[1] - 1))
  if t[0] - 1 >= 0:
    l.append((t[0] - 1, t[1]))
  if t[1] + 1 < myInput[0]:
    l.append((t[0], t[1] + 1))
  if t[0] + 1 < myInput[1]:
    l.append((t[0] + 1, t[1]))
  return l

def BFS(v, myInput):
  state_tab = {}
  dis_tab = {}
  Q = Queue()
  Q.push(v, 0, (myInput[2], ))
  state_tab[(v, (myInput[2],))] = 1
  dis_tab[(v, (myInput[2],))] = 0
  # print("Here")

  while not Q.is_empty():
    v, d, s = Q.pop()
    # print(v)
    # print(d)
    # print(s)

    # pp.pprint(value(v))
    if(value(v) == "E"):
      return dis_tab[(v, s)]

    d = d + 1
    for adjacent in adj(v, myInput):
      adjState = s
      val = value(adjacent)

      l = s[0]
      if val == "M":
        l = l - 1
        adjState = (l, ) + s[1:]

      if "K" in val:
        if not val in adjState:
          adjState = adjState + (val,)

      if "G" in val:
        tmp = val
        tmp = tmp.replace("G", "K")
        if not tmp in adjState:
          continue

      if l == 0  or val == "X":
        continue

      try:
        if state_tab[(adjacent, adjState)] == 1:
          continue
      except:
        # print("Here")
        state_tab[(adjacent, adjState)] = 1
        dis_tab[(adjacent, adjState)] = d
        Q.push(adjacent, d, adjState)

  return -1

def main():
  myInput = map(int, raw_input().split())
  i = myInput[0]
  while i > 0:
    l = raw_input().split()
    graph.append(l)
    i = i - 1

  source = (0,0)
  for j in xrange(0, myInput[0]):
    for k in xrange(0, myInput[1]):
      if graph[j][k] == "S":
        source = (k, j)
        break

  print(BFS(source, myInput))



if __name__=="__main__":
    main()
