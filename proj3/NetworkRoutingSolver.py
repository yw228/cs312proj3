#!/usr/bin/python3


from CS312Graph import *
import time
import math
from arrayMethod import ArrayQueue
from heapMethod import HeapQueue




class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        path_edges = []
        nodes = self.network.getNodes()
        total_length = self.distances[self.dest]
        current = nodes[self.dest]
        one_before = self.previous_nodes[nodes[self.dest]]
        while one_before is not None:
            dist2 = self.distances[current.node_id]
            dist1 = self.distances[one_before.node_id]
            weight = dist2 - dist1
            path_edges.append((current.loc, one_before.loc, '{:.0f}'.format(weight)))
            current = one_before
            one_before = self.previous_nodes[one_before]
        return {'cost': total_length, 'path': path_edges}

    # Dijkstra's algorithm: includes both array queue implementation and min heap implementation
    def computeShortestPaths(self, srcIndex, use_heap):
        self.source = srcIndex
        nodes = self.network.getNodes()
        self.distances = {}
        self.previous_nodes = {}
        for i in nodes:
            self.distances[i.node_id] = math.inf
            self.previous_nodes[i] = None
        self.distances[self.source] = 0

        t1 = time.time()
        if not use_heap:
            self.queue = ArrayQueue()
            self.queue.make_queue(list(self.distances.keys()))
            while self.queue.length > 0:
                node_id = self.queue.deletemin(self.distances)
                if node_id is not None:
                    for edge in nodes[node_id].neighbors:
                        # if current distance is greater than distance if we take another path
                        if self.distances[edge.dest.node_id] > (self.distances[node_id] + edge.length):
                            self.distances[edge.dest.node_id] = self.distances[node_id] + edge.length
                            self.previous_nodes[nodes[edge.dest.node_id]] = nodes[node_id]
                            self.queue.decreasekey()
        else:
            self.queue = HeapQueue()
            self.queue.make_queue(list(self.distances.keys()), self.distances)
            while self.queue.length > 0:
                node_id = self.queue.deletemin(self.distances)
                if node_id is not None:
                    for edge in nodes[node_id].neighbors:
                        if self.distances[edge.dest.node_id] > (self.distances[node_id] + edge.length):
                            self.distances[edge.dest.node_id] = self.distances[node_id] + edge.length
                            self.previous_nodes[nodes[edge.dest.node_id]] = nodes[node_id]
                            self.queue.decreasekey(edge.dest.node_id, self.distances)
        t2 = time.time()
        return t2 - t1

