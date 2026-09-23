"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


class ConfigurationError(RuntimeError):
    """Raised when required application configuration is invalid or missing."""


def get_required_value(name: str) -> str:
    """Return a required non-empty environment value."""
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigurationError(f"Required environment variable {name} is missing.")
    return value.strip()


def get_required_float(name: str) -> float:
    """Return a required environment value converted to a float."""
    value = get_required_value(name)
    try:
        return float(value)
    except ValueError as error:
        raise ConfigurationError(
            f"Environment variable {name} must be a valid numeric coordinate."
        ) from error


def get_optional_positive_float(name: str, default: float) -> float:
    """Return an optional positive float environment value or its default."""
    value = os.getenv(name)
    if value is None or not value.strip():
        return default

    try:
        number = float(value)
    except ValueError as error:
        raise ConfigurationError(
            f"Environment variable {name} must be a valid positive number."
        ) from error

    if number <= 0:
        raise ConfigurationError(f"Environment variable {name} must be greater than zero.")
    return number


class Config:
    """Configuration values for the route application."""

    GOOGLE_MAPS_API_KEY = get_required_value("GOOGLE_MAPS_API_KEY")
    ORIGIN_LAT = get_required_float("ORIGIN_LAT")
    ORIGIN_LNG = get_required_float("ORIGIN_LNG")
    DESTINATION_LAT = get_required_float("DESTINATION_LAT")
    DESTINATION_LNG = get_required_float("DESTINATION_LNG")
    GRAPHML_PATH = Path(os.getenv("GRAPHML_PATH", "data/road_network.graphml"))
    GRAPH_PADDING_KM = get_optional_positive_float("GRAPH_PADDING_KM", default=3.0)
