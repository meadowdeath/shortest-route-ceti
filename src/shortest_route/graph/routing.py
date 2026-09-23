"""Helpers that connect OSMnx graph data to future route algorithms."""

import osmnx as ox

from shortest_route.algorithms.utils import get_minimum_length_edge_data


def find_nearest_node(graph, latitude, longitude):
    """Find the graph node nearest to a geographic coordinate."""
    return ox.distance.nearest_nodes(graph, X=longitude, Y=latitude)


def route_to_coordinates(graph, route):
    """Convert a node route into geometry-aware Google Maps coordinates."""
    if not route:
        return []
    if len(route) == 1:
        return [_node_coordinate(graph, route[0])]

    coordinates = []
    for origin, destination in zip(route, route[1:]):
        for coordinate in _edge_coordinates(graph, origin, destination):
            if not coordinates or coordinate != coordinates[-1]:
                coordinates.append(coordinate)
    return coordinates


def _node_coordinate(graph, node_id):
    """Return a graph node coordinate in Google Maps latitude/longitude order."""
    node_data = graph.nodes[node_id]
    return {"lat": float(node_data["y"]), "lng": float(node_data["x"])}


def _edge_coordinates(graph, origin, destination):
    """Return selected edge geometry, oriented from origin to destination when present."""
    edge_data = get_minimum_length_edge_data(graph, origin, destination)
    origin_coordinate = _node_coordinate(graph, origin)
    destination_coordinate = _node_coordinate(graph, destination)
    geometry = edge_data.get("geometry") if edge_data else None
    geometry_coordinates = getattr(geometry, "coords", None)

    if geometry_coordinates is None:
        return [origin_coordinate, destination_coordinate]

    coordinates = [
        {"lat": float(latitude), "lng": float(longitude)}
        for longitude, latitude, *_ in geometry_coordinates
    ]
    if not coordinates:
        return [origin_coordinate, destination_coordinate]

    if _squared_distance(coordinates[-1], origin_coordinate) < _squared_distance(
        coordinates[0], origin_coordinate
    ):
        coordinates.reverse()
    return coordinates


def _squared_distance(first, second):
    """Return a coordinate-distance comparison value for geometry orientation."""
    return (first["lat"] - second["lat"]) ** 2 + (first["lng"] - second["lng"]) ** 2


def calculate_route(graph, origin, destination, algorithm):
    """Coordinate a future route calculation with the selected algorithm."""
    raise NotImplementedError("Route calculation coordination has not been added yet.")
