"""Manual Dijkstra shortest-path implementation for directed OSMnx graphs."""

from dataclasses import dataclass
import heapq
import math

from shortest_route.algorithms.utils import get_edge_length, reconstruct_path


@dataclass(frozen=True)
class DijkstraResult:
    """Result produced by the manual Dijkstra implementation."""

    path: list
    total_distance: float
    visited_nodes: int


def dijkstra(graph, start, goal):
    """Return the shortest directed path using edge length in meters as the weight."""
    if start not in graph or goal not in graph:
        return None

    distances = {start: 0.0}
    previous = {}
    priority_queue = [(0.0, start)]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue

        visited.add(current_node)
        if current_node == goal:
            path = reconstruct_path(previous, start, goal)
            if path is None:
                return None
            return DijkstraResult(path, current_distance, len(visited))

        for neighbor in graph.successors(current_node):
            if neighbor in visited:
                continue

            edge_length = get_edge_length(graph, current_node, neighbor)
            if edge_length is None or not math.isfinite(edge_length):
                continue

            candidate_distance = current_distance + edge_length
            if candidate_distance < distances.get(neighbor, math.inf):
                distances[neighbor] = candidate_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (candidate_distance, neighbor))

    return None
