'''Advanced form of BFS algorithm

    f(n) -> cost path from start to goal.
    h(n) -> cost path from actual node to goal.
    g(n) -> cost path from start to actual node.

'''


class Graph:

    def __init__(self, adj_list):
        self.adj_list = adj_list

    def get_neighbors(self, v):
        return self.adj_list[v]

    # heuristic consisting of having all nodes with equal values
    def h(self, n):
        H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }
        return H[n]

    def a_star_algorithm(self, start, stop):

        open = set([start])  # visited nodes without all of its neighbors visited
        close = set([])  # visited nodes with all of its neighbots visited

        # has the distances from start to every node
        distances = {}
        distances[start] = 0

        # has an djacent mapping of all nodes
        par = {}
        par[start] = start

        while len(open) > 0:
            n = None

            # find a node with the lowest f(n)
            for v in open:
                if n is None or distances[v] + self.h(v) < distances[n] + self.h(n):
                    n = v

                if n is None:
                    print("No path!")
                    return None

                # if the actual node is the stop, begin from start
                if n == stop:
                    rebuild_path = []

                    while par[n] != n:
                        rebuild_path.append(n)
                        n = par[n]

                    rebuild_path.append(start)
                    rebuild_path.reverse()

                    print("Path found: {}".format(rebuild_path))
                    return rebuild_path

                # for all neighbor nodes of actual node do:
                for (m, weight) in self.get_neighbors(n):
                    if m not in open and m not in close:
                        open.add(m)
                        par[m] = n
                        distances[m] = distances[n] + weight

                    else:
                        if distances[m] > distances[n] + weight:
                            distances[m] = distances[n] + weight
                            par[m] = n

                            if m in close:
                                close.remove(m)
                                open.add(m)

                # remove n form open and add it to close as its neighbors were all visited.
                open.remove(n)
                close.add(n)

        print("Path does not exist")
        return None


adj_list = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)],
}

graph1 = Graph(adj_list)
graph1.a_star_algorithm('A', 'D')
