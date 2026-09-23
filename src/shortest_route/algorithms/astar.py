"""Manual A* shortest-path implementation for directed OSMnx graphs."""

import heapq
from itertools import count
import math

from shortest_route.algorithms.dijkstra import DijkstraResult
from shortest_route.algorithms.utils import (
    geographic_heuristic,
    get_edge_length,
    reconstruct_path,
)


def astar(graph, start, goal):
    """Return the shortest directed path using road distance and Haversine guidance."""
    if start not in graph or goal not in graph:
        return None

    g_score = {start: 0.0}
    previous = {}
    queue_counter = count()
    priority_queue = [(geographic_heuristic(graph, start, goal), next(queue_counter), 0.0, start)]
    visited = set()

    while priority_queue:
        _, _, queued_g_score, current_node = heapq.heappop(priority_queue)
        if queued_g_score > g_score.get(current_node, math.inf):
            continue
        if current_node in visited:
            continue

        visited.add(current_node)
        if current_node == goal:
            path = reconstruct_path(previous, start, goal)
            if path is None:
                return None
            return DijkstraResult(path, queued_g_score, len(visited))

        for neighbor in graph.successors(current_node):
            if neighbor in visited:
                continue

            edge_length = get_edge_length(graph, current_node, neighbor)
            if edge_length is None or not math.isfinite(edge_length):
                continue

            candidate_g_score = queued_g_score + edge_length
            if candidate_g_score < g_score.get(neighbor, math.inf):
                g_score[neighbor] = candidate_g_score
                previous[neighbor] = current_node
                priority = candidate_g_score + geographic_heuristic(graph, neighbor, goal)
                heapq.heappush(
                    priority_queue,
                    (priority, next(queue_counter), candidate_g_score, neighbor),
                )

    return None
