import os
import sys
import pprint
from decimal import Decimal
from collections import deque
from itertools import izip
from operator import itemgetter
import heapq as h
import copy
import math
pp = pprint.PrettyPrinter(indent=4)

def ff(G, e):
  G_resid = copy.deepcopy(G)
  e_resid = copy.deepcopy(e)
  for el in e:
    for el2 in G[el[0]]:
      try:
        G_resid[el2[0]].append((el[0], 0, el2[2]))
      except:
        G_resid[el2[0]] = [(el[0], 0, el2[2])]
    e_resid[(el[1],el[0])] = 0
  res = 0
  while True:
    p, e_resid = ff_find_path(G_resid, e_resid)
    if p == 0:
      break
    res = res + p
  return res

def ff_find_path(G, E):
  S = deque()
  S.append([source])
  V = set()
  frm = {}
  while S:
    p = S.pop()
    u = p[-1]
    if u == sink:
      break
    if u in G:
      for el in G[u]:
        if not el in V:
          if E[(u, el[0])] > 0:
            V.add(el)
            p2 = list(p)
            p2.append(el[0])
            S.append(p2)
  for i in xrange(len(p) - 1):
    frm[p[i+1]] = p[i]
  c = Decimal("infinity")
  where = sink
  while where in frm:
    c = min(c, E[(frm[where],where)])
    where = frm[where]
  where = sink
  while where in frm:
    E[(frm[where], where)] = E[(frm[where], where)] - c
    E[(where, frm[where])] = E[(where, frm[where])] + c
    where = frm[where]
  if c == Decimal("infinity"):
    return 0, {}
  return c, E

def bfs(G, s, t):
  S = deque()
  S.append([s])
  V = set()
  while S:
    p = S.pop()
    u = p[-1]
    if u == t:
      return p
    if u in G:
      for el in G[u]:
        if not el in V:
          V.add(el)
          pp = list(p)
          pp.append(el)
          S.append(pp)

def main():
  inp = map(int, raw_input().split())
  sources = map(int, raw_input().split())
  starting_pop = map(int, raw_input().split())
  starting_positions = {}
  for el in sources:
    for el2 in starting_pop:
      starting_positions[el] = el2
  desire = sum(starting_pop)
  dests = map(int, raw_input().split())
  G = {}
  F = {}
  V = []
  for i in xrange(inp[3]):
    tmp = map(int, raw_input().split())
    if not tmp[0] in V:
      V.append(tmp[0])
    if not tmp[1] in V:
      V.append(tmp[1])
    F[(tmp[0], tmp[1])] = (tmp[2], tmp[3])
    if tmp[0] in G:
      G[tmp[0]].append(tmp[1])
    else:
      G[tmp[0]] = [(tmp[1])]
  global sink
  sink = "t"
  global source
  source = "s"
  already_searched = set()
  paths = []
  for el in sources:
    for el2 in dests:
      path = bfs(G, el, el2)
      if path:
        if path[-1] == el2:
          paths.append(path)
          break
  if not len(paths) == len(sources):
    print(-1)
    return
  upper_bound = 0
  for path in paths:
    path_bound = 0
    m = Decimal("infinity")
    for i in xrange(len(path) - 1):
      path_bound = path_bound + F[(path[i],path[i+1])][1]
      if F[(path[i],path[i+1])][0] < m:
        m = F[(path[i],path[i+1])][0]
    upper_bound = int(upper_bound + math.ceil(((float(starting_positions[path[0]])/m) * path_bound)))
  maximum = upper_bound
  min_time = 0
  max_time = upper_bound
  min_success = Decimal("infinity")
  while(max_time >= min_time):
    mid_time = int(math.ceil((float((min_time + max_time)) / 2)))
    g = {}
    e = {}
    g[source] = []
    for i in V:
      for j in xrange(mid_time - 1):
        g[i, j] = [((i, j + 1), Decimal("infinity"), 0)]
        e[((i, j),(i, j + 1))] = Decimal("infinity")
    for i in xrange(mid_time):
      for key in F:
        if i + F[key][1] <= mid_time:
          if (key[0], i) in g:
            g[(key[0],i)].append(((key[1], i+F[key][1]), F[key][0], 0))
            e[((key[0],i), (key[1], i+F[key][1]))] = F[key][0]
            if key[0] in sources:
              g[source].append(((key[0],i),Decimal("infinity"), 0))
              e[((source), (key[0],i))] = Decimal("infinity")
            if key[1] in dests:
              g[(key[1], i+F[key][1])] = [((sink),Decimal("infinity"), 0)]
              e[((key[1], i+F[key][1]), sink)] = Decimal("infinity")
          else:
            g[(key[0],i)] = [((key[1], i+F[key][1]), F[key][0], 0)]
            e[((key[0],i), (key[1], i+F[key][1]))] = F[key][0]
            if key[0] in sources:
              g[source].append(((key[0],i),Decimal("infinity"), 0))
              e[((source), (key[0],i))] = Decimal("infinity")
            if key[1] in dests:
              g[(key[1], i+F[key][1])] = [((sink),Decimal("infinity"), 0)]
              e[((key[1], i+F[key][1]), sink)] = Decimal("infinity")

    mf = ff(g, e)
    if mf < desire:
      min_time = mid_time + 1
    if mf >= desire:
      if mid_time < min_success:
        min_success = mid_time
      max_time = mid_time - 1

  if min_success == Decimal("infinity"):
    print(-1)
  else:
    print(min_success)

if __name__=="__main__":
    main()
