"""OSMnx road-network download and local GraphML persistence helpers."""

import math
from pathlib import Path

import osmnx as ox


def calculate_download_bbox(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
    padding_km: float,
) -> tuple[float, float, float, float]:
    """Return an OSMnx bbox covering both locations plus a geographic margin.

    The tuple order is west, south, east, north, which is the OSMnx v2 bbox order.
    """
    if padding_km <= 0:
        raise ValueError("Padding must be greater than zero.")

    mean_latitude = (origin_lat + destination_lat) / 2
    latitude_padding = padding_km / 111.32
    longitude_padding = padding_km / (
        111.32 * max(math.cos(math.radians(mean_latitude)), 0.01)
    )

    west = min(origin_lng, destination_lng) - longitude_padding
    south = min(origin_lat, destination_lat) - latitude_padding
    east = max(origin_lng, destination_lng) + longitude_padding
    north = max(origin_lat, destination_lat) + latitude_padding
    return west, south, east, north


def download_road_network(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
    padding_km: float,
):
    """Download a driving MultiDiGraph covering both configured locations.

    This function performs a network request and must only be called explicitly by
    the manual download command, never during normal Flask requests.
    """
    bbox = calculate_download_bbox(
        origin_lat,
        origin_lng,
        destination_lat,
        destination_lng,
        padding_km,
    )
    return ox.graph_from_bbox(bbox=bbox, network_type="drive", retain_all=True)


def save_road_network(graph, path: Path | str) -> Path:
    """Save an OSMnx graph as GraphML and return its path."""
    graph_path = Path(path)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(graph, filepath=graph_path)
    return graph_path


def load_road_network(path: Path | str):
    """Load an existing GraphML road network without downloading data."""
    graph_path = Path(path)
    if not graph_path.is_file():
        raise FileNotFoundError(
            "No se encontró la red vial local. Ejecute el comando de descarga manual "
            "antes de calcular rutas."
        )
    return ox.load_graphml(filepath=graph_path)


def main() -> None:
    """Explicitly download and persist the configured driving road network."""
    from shortest_route.config import Config

    print("Descargando red vial...")
    graph = download_road_network(
        origin_lat=Config.ORIGIN_LAT,
        origin_lng=Config.ORIGIN_LNG,
        destination_lat=Config.DESTINATION_LAT,
        destination_lng=Config.DESTINATION_LNG,
        padding_km=Config.GRAPH_PADDING_KM,
    )
    saved_path = save_road_network(graph, Config.GRAPHML_PATH)
    print(f"Red vial guardada en {saved_path}")


if __name__ == "__main__":
    main()
