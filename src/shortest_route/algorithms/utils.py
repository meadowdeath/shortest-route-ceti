"""Shared helpers for manual routing algorithms."""

import math


def reconstruct_path(came_from, start, goal):
    """Reconstruct a path from predecessor data."""
    if start == goal:
        return [start]
    if goal not in came_from:
        return None

    path = [goal]
    current_node = goal
    while current_node != start:
        current_node = came_from.get(current_node)
        if current_node is None:
            return None
        path.append(current_node)

    path.reverse()
    return path


def get_edge_length(graph, origin, destination):
    """Return the length of an edge selected by a future algorithm."""
    edge_data = get_minimum_length_edge_data(graph, origin, destination)
    if edge_data is None:
        return None
    return float(edge_data["length"])


def get_minimum_length_edge_data(graph, origin, destination):
    """Return attributes for the shortest valid directed edge from origin to destination."""
    parallel_edges = graph.get_edge_data(origin, destination)
    if not parallel_edges:
        return None

    edge_candidates = [parallel_edges] if "length" in parallel_edges else parallel_edges.values()
    valid_edges = []
    for edge_attributes in edge_candidates:
        if not isinstance(edge_attributes, dict):
            continue
        length = edge_attributes.get("length")
        if isinstance(length, bool):
            continue
        try:
            numeric_length = float(length)
        except (TypeError, ValueError):
            continue
        if math.isfinite(numeric_length) and numeric_length >= 0:
            valid_edges.append((numeric_length, edge_attributes))

    if not valid_edges:
        return None
    return min(valid_edges, key=lambda item: item[0])[1]


def haversine_distance(latitude_a, longitude_a, latitude_b, longitude_b):
    """Return the great-circle distance between coordinates in meters."""
    earth_radius_m = 6_371_000
    latitude_delta = math.radians(latitude_b - latitude_a)
    longitude_delta = math.radians(longitude_b - longitude_a)
    latitude_a_radians = math.radians(latitude_a)
    latitude_b_radians = math.radians(latitude_b)

    haversine_value = (
        math.sin(latitude_delta / 2) ** 2
        + math.cos(latitude_a_radians)
        * math.cos(latitude_b_radians)
        * math.sin(longitude_delta / 2) ** 2
    )
    haversine_value = min(1.0, max(0.0, haversine_value))
    central_angle = 2 * math.atan2(math.sqrt(haversine_value), math.sqrt(1 - haversine_value))
    return earth_radius_m * central_angle


def geographic_heuristic(graph, current, goal):
    """Estimate a graph-node straight-line distance in meters using Haversine."""
    current_data = graph.nodes[current]
    goal_data = graph.nodes[goal]
    return haversine_distance(
        float(current_data["y"]),
        float(current_data["x"]),
        float(goal_data["y"]),
        float(goal_data["x"]),
    )
