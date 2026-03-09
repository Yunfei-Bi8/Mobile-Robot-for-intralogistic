# Gives the fastest route from [startnode] to [endnote] for a [graph]
def dijkstra(graph,startnode,endnode):
    D = {}
    R = {}
    # automatically fill graph
    for node in graph:
        D[node] = 9999
        R[node] = []
    
    D[startnode] = 0
    MK = [startnode]

    while len(MK) != 0:

        # 1
        dis_start = 999999
        for node in MK:
            dis_start_node = D[node]
            if dis_start_node < dis_start:
                new_node = node
                dis_start = dis_start_node
        current_node = new_node

        # 2
        for neighbour in graph[current_node]:
            if D[neighbour] > D[current_node] + graph[current_node][neighbour]:
                D[neighbour] = D[current_node] + graph[current_node][neighbour]
                R[neighbour].clear()
                R[neighbour].append(current_node)                
                MK.append(neighbour)
                R[neighbour].extend(R[current_node])

        # 3
        MK.remove(current_node)

    for node in R:
        R[node].insert(0,node)
    route = R[endnode]
    route.reverse()
    return route