"""
Minimum directed spanning tree
"""
from collections import deque

INF = 1000000
def find_abrorescential(n, r, edges):
    """function to find the minimum directed spanning tree"""

    def bfs_reachable(n, r, edges):
        """bfs for all reachable verticies from root"""
        adj = {v: [] for v in range(1, n + 1)}
        for u, v, w in edges:
            adj[u].append(v)

        visited = set()
        q = deque([r])
        visited.add(r)

        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)

        return visited

    def find_cycle(reach, min_e, r):
        """Test for a cycle"""
        for v in reach:
            if v == r:
                continue

            active = []
            seen = set()
            curr = v

            while curr > 0 and curr not in seen:
                active.append(curr)
                seen.add(curr)
                curr = min_e[curr][0]

            if curr > 0 and curr in seen:
                cycle = []
                for x in reversed(active):
                    cycle.append(x)
                    if x == curr:
                        break

                cycle.reverse()
                return cycle
        return None

    reachable = bfs_reachable(n, r, edges)
    edges = [(u, v, w) for (u, v, w) in edges if u in reachable and v in reachable]

    minimal_edge = [(-1, -1)] + [(0, INF)] * n
    minimal_edge[r] = (0,0)
    for u, v, w in edges:
        if v not in reachable:
            continue
        if v != r and minimal_edge[v][1] > w:
            minimal_edge[v] = (u, w)
    
    cycle = find_cycle(reachable, minimal_edge, r)
    if not cycle:
        return minimal_edge

    new_edges = []
    c_id = n + 1
    cycle_set = set(cycle)

    incoming_e = {}

    for u, v, w in edges:
        if v in cycle_set and u in cycle_set: continue
        if u in cycle_set and v not in cycle_set:
            # outside of cycle vert
            new_edges.append((c_id, v, w))
        elif v in cycle_set and u not in cycle_set:
            # inside  of cycle vert
            w_adj = w - minimal_edge[v][1]
            new_edges.append((u, c_id, w_adj))
            if (u, c_id) not in incoming_e or w_adj < incoming_e[(u, c_id)][2]:
                incoming_e[(u, c_id)] = (v, w, w_adj)
        else:
            new_edges.append((u, v, w))

    new_r = r
    if r in cycle_set:
        new_r = c_id
    res_contracted = find_abrorescential(n+1, new_r, new_edges)
    
    parent = res_contracted
    parent_final = [(-1, -1)] * (n+1)
    c_u, _ = parent[c_id]

    def expand_outgoing_parent(v, p_v, w_v):
        if p_v != c_id:
            return (p_v, w_v)
        for u0, v0, w0 in edges:
            if v0 == v and u0 in cycle_set and w0 == w_v:
                return (u0, w0)
        return (p_v, w_v)

    if c_u != 0:
        real_v, w_orig, _ = incoming_e[(c_u, c_id)]

        for v in range(1, n+1):
            if v in cycle_set:
                if v == real_v:
                    parent_final[v] = (c_u, w_orig)
                else:
                    parent_final[v] = minimal_edge[v]
            else:
                p_v, w_v = parent[v]
                parent_final[v] = expand_outgoing_parent(v, p_v, w_v)
    else:
        if r in cycle_set:
            root_cycle = r
        else:
            root_cycle = cycle[0]

        for v in range(1, n+1):
            if v in cycle_set:
                if v == root_cycle:
                    parent_final[v] = (0,0)
                else:
                    parent_final[v] = minimal_edge[v]
            else:
                p_v, w_v = parent[v]
                parent_final[v] = expand_outgoing_parent(v, p_v, w_v)
    return parent_final

def calculate_graph_weight(edges):
    graph_weight = 0
    for p, w in edges:
        if p == -1:
            continue
        if p != 0:
            graph_weight += w
    return graph_weight



if __name__ == '__main__':
    num = 3
    root = 1
    edges_test = {
        (3, 1, 9),
        (2, 1, 6),
        (2, 3, 8),
        (1, 3, 13),
    }

    res = find_abrorescential(num, root, edges_test)
    result = res[1:]
    w = calculate_graph_weight(res)
    print(result, w)
