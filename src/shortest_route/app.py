"""Flask application entry points."""

import time

from flask import Flask, jsonify, render_template

from shortest_route.algorithms.astar import astar
from shortest_route.algorithms.dijkstra import dijkstra
from shortest_route.config import Config
from shortest_route.graph.loader import load_road_network
from shortest_route.graph.routing import find_nearest_node, route_to_coordinates


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/")
    def index():
        """Render the main route-planning page."""
        return render_template(
            "index.html",
            google_maps_api_key=app.config["GOOGLE_MAPS_API_KEY"],
            origin_lat=app.config["ORIGIN_LAT"],
            origin_lng=app.config["ORIGIN_LNG"],
            destination_lat=app.config["DESTINATION_LAT"],
            destination_lng=app.config["DESTINATION_LNG"],
        )

    @app.get("/api/routes/dijkstra")
    def calculate_dijkstra_route():
        """Calculate a local road-network route using manual Dijkstra."""
        try:
            graph = load_road_network(app.config["GRAPHML_PATH"])
        except FileNotFoundError:
            return jsonify(error="No se encontró la red vial local."), 503
        except (OSError, ValueError, TypeError):
            return jsonify(error="No se pudo cargar la red vial local."), 422

        try:
            origin_node = find_nearest_node(
                graph, app.config["ORIGIN_LAT"], app.config["ORIGIN_LNG"]
            )
            destination_node = find_nearest_node(
                graph, app.config["DESTINATION_LAT"], app.config["DESTINATION_LNG"]
            )
            start_time = time.perf_counter()
            result = dijkstra(graph, origin_node, destination_node)
            execution_ms = (time.perf_counter() - start_time) * 1000

            if result is None:
                return jsonify(error="No se pudo calcular la ruta."), 404

            return jsonify(
                algorithm="dijkstra",
                distance_m=result.total_distance,
                visited_nodes=result.visited_nodes,
                execution_ms=execution_ms,
                path=route_to_coordinates(graph, result.path),
            )
        except (KeyError, TypeError, ValueError):
            return jsonify(error="La red vial local no es válida."), 422
        except Exception:
            return jsonify(error="Ocurrió un error al calcular la ruta."), 500

    @app.get("/api/routes/astar")
    def calculate_astar_route():
        """Calculate a local road-network route using manual A*."""
        try:
            graph = load_road_network(app.config["GRAPHML_PATH"])
        except FileNotFoundError:
            return jsonify(error="No se encontró la red vial local."), 503
        except (OSError, ValueError, TypeError):
            return jsonify(error="No se pudo cargar la red vial local."), 422

        try:
            origin_node = find_nearest_node(
                graph, app.config["ORIGIN_LAT"], app.config["ORIGIN_LNG"]
            )
            destination_node = find_nearest_node(
                graph, app.config["DESTINATION_LAT"], app.config["DESTINATION_LNG"]
            )
            start_time = time.perf_counter()
            result = astar(graph, origin_node, destination_node)
            execution_ms = (time.perf_counter() - start_time) * 1000

            if result is None:
                return jsonify(error="No se pudo calcular la ruta."), 404

            return jsonify(
                algorithm="astar",
                distance_m=result.total_distance,
                visited_nodes=result.visited_nodes,
                execution_ms=execution_ms,
                path=route_to_coordinates(graph, result.path),
            )
        except (KeyError, TypeError, ValueError):
            return jsonify(error="La red vial local no es válida."), 422
        except Exception:
            return jsonify(error="Ocurrió un error al calcular la ruta."), 500

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
