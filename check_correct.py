import random
from collections import defaultdict, deque

import networkx as nx

from solution import find_abrorescential, calculate_graph_weight


def bfs_reachable(n, r, edges):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append(v)

    q = deque([r])
    vis = {r}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in vis:
                vis.add(v)
                q.append(v)
    return vis


def nx_arborescence_weight(n, r, edges):
    reachable = bfs_reachable(n, r, edges)
    if not reachable:
        return 0, []

    filtered_edges = [(u, v, w) for (u, v, w) in edges if u in reachable and v in reachable]

    if len(reachable) == 1:
        return 0, []

    max_w = max(w for _, _, w in filtered_edges) if filtered_edges else 0
    bigM = max_w * (n + 5) + 1

    G = nx.DiGraph()
    S = 0

    for u, v, w in filtered_edges:
        G.add_edge(u, v, weight=w)

    for v in reachable:
        if v == r:
            G.add_edge(S, v, weight=0)
        else:
            G.add_edge(S, v, weight=bigM)

    arb = nx.minimum_spanning_arborescence(G, attr="weight", default=0)

    result_edges = []
    total_weight = 0
    for u, v, data in arb.edges(data=True):
        if u == S or v == S:
            continue
        w = data.get("weight", 0)
        result_edges.append((u, v, w))
        total_weight += w

    return total_weight, result_edges


def random_graph(n, p=0.4, max_w=20):
    edges = set()
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u == v:
                continue
            if random.random() < p:
                edges.add((u, v, random.randint(1, max_w)))
    return list(edges)


def compare_single_graph(n, r, edges, verbose=True):
    # the one by me
    parent_arr = find_abrorescential(n, r, edges)
    parent_arr = parent_arr[1:]
    my_w = calculate_graph_weight(parent_arr)
    my_edges = parent_arr

    #networkx
    nx_w, nx_edges = nx_arborescence_weight(n, r, edges)

    ok = (my_w == nx_w)
    if verbose:
        print("n =", n, "root =", r)
        print("Edges:")
        for e in sorted(edges):
            print(" ", e)
        print("\nMy result:")
        print("  weight:", my_w)
        print("  edges :", sorted(my_edges))
        print("\nNetworkX result:")
        print("  weight:", nx_w)
        print("  edges :", sorted(nx_edges))
        print("\nMATCH:" if ok else "\nMISMATCH!")

    return ok


def stress_test(num_tests=200, n_min=2, n_max=10, seed=0):
    random.seed(seed)
    for test_id in range(1, num_tests + 1):
        n = random.randint(n_min, n_max)
        r = random.randint(1, n)
        edges = random_graph(n, p=0.4, max_w=20)

        if not any(u == r for u, v, w in edges):
            for v in range(1, n + 1):
                if v != r:
                    edges.append((r, v, random.randint(1, 20)))
                    break

        ok = compare_single_graph(n, r, edges, verbose=False)
        if not ok:
            print("=== MISMATCH ON TEST", test_id, "===")
            compare_single_graph(n, r, edges, verbose=True)
            return
    print("YAPPIEEE, all ", num_tests, "results are checked by networkx and are correct!")

if __name__ == "__main__":
    stress_test(num_tests=300)
