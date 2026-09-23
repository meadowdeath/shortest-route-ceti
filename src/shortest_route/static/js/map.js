"use strict";

let mapInstance = null;
let originMarker = null;
let destinationMarker = null;
let routeOverlay = null;

function getStatusContainer() {
  return document.getElementById("route-status");
}

function fitLocations() {
  const { origin, destination } = window.mapConfiguration;
  const bounds = new google.maps.LatLngBounds();

  bounds.extend(origin);
  bounds.extend(destination);
  mapInstance.fitBounds(bounds, 80);
}

async function initializeMap() {
  const statusContainer = getStatusContainer();

  try {
    const { Map } = await google.maps.importLibrary("maps");
    const { origin, destination } = window.mapConfiguration;

    mapInstance = new Map(document.getElementById("map"), {
      center: origin,
      zoom: 14,
    });

    originMarker = new google.maps.Marker({
      map: mapInstance,
      position: origin,
      title: "Origen",
    });
    destinationMarker = new google.maps.Marker({
      map: mapInstance,
      position: destination,
      title: "CETI Colomos",
    });

    fitLocations();
  } catch (error) {
    statusContainer.textContent = "No se pudo cargar el mapa.";
  }
}

function displayRoute(routeCoordinates) {
  if (!mapInstance || routeCoordinates.length === 0) {
    return;
  }

  if (routeOverlay) {
    routeOverlay.setMap(null);
  }

  routeOverlay = new google.maps.Polyline({
    path: routeCoordinates,
    strokeColor: "#1a73e8",
    strokeOpacity: 0.9,
    strokeWeight: 5,
    map: mapInstance,
  });

  const bounds = new google.maps.LatLngBounds();
  routeCoordinates.forEach((coordinate) => bounds.extend(coordinate));
  mapInstance.fitBounds(bounds, 80);
}

function resetRoute() {
  if (routeOverlay) {
    routeOverlay.setMap(null);
    routeOverlay = null;
  }

  if (mapInstance) {
    fitLocations();
  }
}

async function calculateRoute(endpoint, algorithmName, button, statusContainer) {
  button.disabled = true;
  statusContainer.textContent = `Calculando ruta con ${algorithmName}...`;

  try {
    const response = await fetch(endpoint);
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "No se pudo calcular la ruta.");
    }

    displayRoute(payload.path);
    statusContainer.textContent = [
      `Algoritmo: ${algorithmName}`,
      `Distancia total: ${(payload.distance_m / 1000).toFixed(2)} km`,
      `Nodos explorados: ${payload.visited_nodes}`,
      `Tiempo de ejecución: ${payload.execution_ms.toFixed(3)} ms`,
    ].join("\n");
  } catch (error) {
    statusContainer.textContent = error.message || "No se pudo calcular la ruta.";
  } finally {
    button.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const statusContainer = document.getElementById("route-status");
  const dijkstraButton = document.getElementById("dijkstra-button");
  const astarButton = document.getElementById("astar-button");
  const resetButton = document.getElementById("reset-button");

  dijkstraButton.addEventListener("click", async () => {
    await calculateRoute(
      "/api/routes/dijkstra",
      "Dijkstra",
      dijkstraButton,
      statusContainer,
    );
  });

  astarButton.addEventListener("click", async () => {
    await calculateRoute("/api/routes/astar", "A*", astarButton, statusContainer);
  });

  resetButton.addEventListener("click", () => {
    resetRoute();
    statusContainer.textContent = "";
  });
});

window.initializeMap = initializeMap;
