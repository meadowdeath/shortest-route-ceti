"""Tests for graph-route coordinate helpers that do not require network access."""

import networkx as nx

from shortest_route.graph import routing


def test_route_to_coordinates_returns_valid_coordinate_structures():
    """Verify conversion produces Google Maps-compatible coordinate dictionaries."""
    graph = nx.MultiDiGraph()
    graph.add_node(1, y=20.0, x=-103.0)
    graph.add_node(2, y=20.1, x=-103.1)
    graph.add_edge(1, 2, length=1)

    coordinates = routing.route_to_coordinates(graph, [1, 2])

    assert coordinates == [
        {"lat": 20.0, "lng": -103.0},
        {"lat": 20.1, "lng": -103.1},
    ]


def test_route_to_coordinates_uses_edge_geometry_in_latitude_longitude_order():
    """Verify edge geometry follows the road shape instead of a straight node line."""
    geometry = type(
        "LineString",
        (),
        {"coords": [(-103.0, 20.0), (-103.05, 20.02), (-103.1, 20.1)]},
    )()
    graph = nx.MultiDiGraph()
    graph.add_node(1, y=20.0, x=-103.0)
    graph.add_node(2, y=20.1, x=-103.1)
    graph.add_edge(1, 2, length=1, geometry=geometry)

    coordinates = routing.route_to_coordinates(graph, [1, 2])

    assert coordinates == [
        {"lat": 20.0, "lng": -103.0},
        {"lat": 20.02, "lng": -103.05},
        {"lat": 20.1, "lng": -103.1},
    ]


def test_find_nearest_node_uses_longitude_as_x_and_latitude_as_y(monkeypatch):
    """Verify OSMnx nearest-node parameters follow its X/Y coordinate convention."""
    captured_arguments = {}

    def fake_nearest_nodes(graph, X, Y):
        captured_arguments.update({"graph": graph, "X": X, "Y": Y})
        return "nearest-node"

    monkeypatch.setattr(routing.ox.distance, "nearest_nodes", fake_nearest_nodes)
    graph = object()

    result = routing.find_nearest_node(graph, latitude=20.7, longitude=-103.4)

    assert result == "nearest-node"
    assert captured_arguments == {"graph": graph, "X": -103.4, "Y": 20.7}
