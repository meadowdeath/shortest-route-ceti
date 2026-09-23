"""Deterministic tests for the manual Dijkstra implementation."""

import networkx as nx

from shortest_route.algorithms.dijkstra import dijkstra


def test_dijkstra_returns_the_shortest_directed_route():
    """Verify Dijkstra chooses the route with the smallest total edge length."""
    graph = nx.MultiDiGraph()
    graph.add_edge("A", "B", length=2)
    graph.add_edge("B", "D", length=3)
    graph.add_edge("A", "C", length=10)
    graph.add_edge("C", "D", length=1)

    result = dijkstra(graph, "A", "D")

    assert result is not None
    assert result.path == ["A", "B", "D"]
    assert result.total_distance == 5
    assert result.visited_nodes == 3


def test_dijkstra_uses_the_shortest_valid_parallel_edge():
    """Verify parallel MultiDiGraph edges use their minimum valid length."""
    graph = nx.MultiDiGraph()
    graph.add_edge("A", "B", length=10)
    graph.add_edge("A", "B", length=2)
    graph.add_edge("B", "D", length=3)

    result = dijkstra(graph, "A", "D")

    assert result is not None
    assert result.path == ["A", "B", "D"]
    assert result.total_distance == 5


def test_dijkstra_returns_none_for_an_unreachable_destination():
    """Verify Dijkstra does not fabricate a path when no directed route exists."""
    graph = nx.MultiDiGraph()
    graph.add_edge("A", "B", length=2)
    graph.add_node("D")

    assert dijkstra(graph, "A", "D") is None
