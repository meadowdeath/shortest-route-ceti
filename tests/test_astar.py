"""Deterministic tests for the manual A* implementation."""

import networkx as nx
import pytest

from shortest_route.algorithms.astar import astar
from shortest_route.algorithms.dijkstra import dijkstra
from shortest_route.algorithms.utils import geographic_heuristic


def build_test_graph():
    """Build a graph whose edge lengths exceed straight-line distances."""
    graph = nx.MultiDiGraph()
    graph.add_node("A", y=0.0, x=0.0)
    graph.add_node("B", y=0.0, x=0.001)
    graph.add_node("C", y=0.001, x=0.0)
    graph.add_node("D", y=0.0, x=0.002)
    graph.add_edge("A", "B", length=120)
    graph.add_edge("B", "D", length=120)
    graph.add_edge("A", "C", length=400)
    graph.add_edge("C", "D", length=400)
    return graph


def test_astar_returns_the_shortest_directed_route():
    """Verify A* selects the lowest-cost directed route."""
    result = astar(build_test_graph(), "A", "D")

    assert result is not None
    assert result.path == ["A", "B", "D"]
    assert result.total_distance == 240


def test_astar_matches_dijkstra_optimal_cost():
    """Verify A* and Dijkstra return the same optimum on a deterministic graph."""
    graph = build_test_graph()

    dijkstra_result = dijkstra(graph, "A", "D")
    astar_result = astar(graph, "A", "D")

    assert dijkstra_result is not None
    assert astar_result is not None
    assert astar_result.total_distance == pytest.approx(dijkstra_result.total_distance)
    assert astar_result.path == dijkstra_result.path


def test_astar_returns_none_for_an_unreachable_destination():
    """Verify A* does not fabricate a route when directed connectivity is absent."""
    graph = build_test_graph()
    graph.remove_edge("B", "D")
    graph.remove_edge("C", "D")

    assert astar(graph, "A", "D") is None


def test_astar_uses_the_shortest_valid_parallel_edge():
    """Verify A* evaluates the minimum valid length among parallel edges."""
    graph = nx.MultiDiGraph()
    graph.add_node("A", y=0.0, x=0.0)
    graph.add_node("B", y=0.0, x=0.001)
    graph.add_node("D", y=0.0, x=0.002)
    graph.add_edge("A", "B", length=500)
    graph.add_edge("A", "B", length=120)
    graph.add_edge("B", "D", length=120)

    result = astar(graph, "A", "D")

    assert result is not None
    assert result.path == ["A", "B", "D"]
    assert result.total_distance == 240


def test_geographic_heuristic_is_zero_at_goal_and_positive_elsewhere():
    """Verify the Haversine graph heuristic has the expected basic behavior."""
    graph = build_test_graph()

    assert geographic_heuristic(graph, "D", "D") == pytest.approx(0)
    assert geographic_heuristic(graph, "A", "D") > 0
