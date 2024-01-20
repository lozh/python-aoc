#!/usr/bin/env python3

import sys
import re
from collections import defaultdict
from dataclasses import dataclass, field
import math
from heapq import heappush, heappop

@dataclass(order=True)
class Priority:
    priority: int
    item: str = field(compare=False)

def cut_of_the_phase(vertices, edges, a):
    aset = {a}
    t = a
    rest = []
    entry_finder = {}

    for v in vertices:
        if v != a:
            # use negative priority as we need to find max
            entry = Priority(-edges[a][v] if v in edges[a] else 0, v)
            entry_finder[v] = entry
            heappush(rest, entry)

    while len(aset) < len(vertices):
        s = t
        while not (t:= heappop(rest).item):
            pass
        del entry_finder[t]
        aset.add(t)
        for v in edges[t]:
            if v not in aset:
                # update priority by tombstoning and re-adding
                entry = entry_finder.pop(v)
                entry.item = None
                entry = Priority(entry.priority - edges[t][v], v)
                entry_finder[v] = entry
                heappush(rest, entry)
    return s, t

def merge_vertices(vertices, edges, s, t):
    vertices[s].extend(vertices[t])
    del vertices[t]
    for v in edges[t]:
        if s != v:
            w = edges[t][v] + edges[s].get(v, 0)
            edges[s][v] = w
            edges[v][s] = w
    for v in edges[t]:
        del edges[v][t]
    del edges[t]

def stoer_wagner(vertices, edges):
    # for something general purpose, we should clone the inputs
    # pick a random vertex
    a = next(iter(vertices))
    min_cut_size = math.inf
    min_cut = None
    while len(vertices) > 1:
        s, t = cut_of_the_phase(vertices, edges, a)
        cut_size = sum(edges[t][v] for v in edges[t])
        if cut_size < min_cut_size:
            min_cut_size = cut_size
            min_cut = vertices[t]
        # merge s and t
        merge_vertices(vertices, edges, s, t)
    return min_cut_size, min_cut

def parse(lines):
    vertices = {}
    edges = defaultdict(dict)
    for line in lines:
        m = re.match(r"(\w+): (.*)$", line)
        f = m[1]
        if not f in vertices:
            vertices[f] = [f]
        for t in str.split(m[2], " "):
            if not t in vertices:
                vertices[t] = [t]
            edges[f][t] = 1
            edges[t][f] = 1
    return(vertices, edges)

vertices, edges = parse(map(str.rstrip, sys.stdin))
vcount = len(vertices)
cut = stoer_wagner(vertices, edges)
ccount = len(cut[1])
print(ccount * (vcount - ccount))
