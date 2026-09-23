# Shortest Route to CETI Colomos

This university assignment will calculate the shortest driving route from a configured fixed origin to CETI Colomos. It will provide two academically important, manually implemented algorithms: Dijkstra and A*. Google Maps JavaScript API will visualize the route returned by the Python application.

Google Maps is only responsible for visualizing the calculated route. Shortest-path computation will be performed by the Python implementations of Dijkstra and A*, not by Google Directions or Google Routes APIs.

Dijkstra and A* are implemented manually and use each directed road edge's `length` attribute (meters) as their weight. A* uses a geographic Haversine-distance heuristic to guide the same distance optimization. Google Maps only draws the returned route geometry; it does not calculate the shortest path.

## Architecture

The project uses a small `src` layout:

- `src/shortest_route/app.py`: Flask application and web-page route.
- `src/shortest_route/config.py`: environment-based application configuration.
- `src/shortest_route/algorithms/`: isolated manual Dijkstra and A* implementations plus shared helpers.
- `src/shortest_route/graph/`: OSMnx graph persistence and route-coordinate integration.
- `src/shortest_route/templates/` and `static/`: the minimal browser interface.
- `tests/`: future deterministic tests for the algorithms and routing conversion.
- `data/`: local generated road-network files.

## Technologies

- Python 3.12
- Flask
- OSMnx and its NetworkX graph support
- python-dotenv
- pytest
- Google Maps JavaScript API

## Setup assumptions

The Conda environment already exists and is named `shortest-route`; this repository does not create it or install packages. `environment.yml` is concise reproducibility documentation, not an exported environment snapshot.

Activate the existing environment before doing development work:

```powershell
conda activate shortest-route
```

Copy `.env.example` to `.env` and supply the required configuration values locally. Never commit `.env`.

Generated `.graphml` road-network files are ignored by Git because they can be large, machine-generated cache artifacts and can be regenerated from the configured graph-loading workflow.

## Road-network download

The application uses a driving-road graph from OpenStreetMap, downloaded through OSMnx. Google Maps is used only to visualize locations and future calculated routes.

With the existing `shortest-route` environment active and `.env` configured, download the road network explicitly from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m shortest_route.graph.loader
```

This downloads a driving graph that covers both configured locations plus a configurable margin (default: 3 km), then saves it as `data/road_network.graphml`. The application never downloads this graph during a Flask request; future routing work will load the saved local GraphML file.

Start the Flask application afterward with:

```powershell
$env:PYTHONPATH = "src"
flask --app shortest_route.app:create_app run
```

## Planned development sequence

1. Initial project structure
2. Flask application setup
3. Road-network loading with OSMnx
4. Manual Dijkstra implementation
5. Dijkstra tests
6. Manual A* implementation
7. A* tests
8. Routing API integration
9. Google Maps integration
10. Route visualization and reset behavior
11. Final testing and cleanup
