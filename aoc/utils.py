from gridgraphs import (
    BreadthFirstStrategy,
    Cardinal,
    DepthFirstStrategy,
    Diagonal,
    GridGraph,
    get_island_stats,
)


def test_grid_graph() -> None:
    graph = GridGraph.create_graph(rows=50, cols=50)
    for direction in [Diagonal, Cardinal]:
        for strategy in [DepthFirstStrategy, BreadthFirstStrategy]:
            print(f"{strategy.__name__} {direction.__name__}")
            stats = get_island_stats(graph, strategy(), direction)
            print(stats)
            graph.clear_visited()
