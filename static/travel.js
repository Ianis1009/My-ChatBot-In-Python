let routeMap = null;
let routeLine = null;
let originMarker = null;
let destinationMarker = null;

const routeForm = document.getElementById("route-form");

const originInput = document.getElementById("origin");
const destinationInput = document.getElementById("destination");

const calculateButton =
    document.getElementById("calculate-route");

const routeResult =
    document.getElementById("route-result");

const routeError =
    document.getElementById("route-error");

const routeSummary =
    document.getElementById("route-summary");

const distanceElement =
    document.getElementById("distance");

const durationElement =
    document.getElementById("duration");

const errorMessage =
    document.getElementById("error-message");

const speakRouteButton =
    document.getElementById("speak-route");


let currentVoiceMessage = "";


function initializeRouteMap() {

    if (routeMap) {
        return;
    }

    routeMap = L.map("route-map");

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(routeMap);
}


function displayRouteMap(route) {

    const mapContainer = document.getElementById("route-map");

    mapContainer.classList.remove("hidden");

    initializeRouteMap();

    if (routeLine) {
        routeMap.removeLayer(routeLine);
    }

    if (originMarker) {
        routeMap.removeLayer(originMarker);
    }

    if (destinationMarker) {
        routeMap.removeLayer(destinationMarker);
    }

    const coordinates = route.geometry.coordinates;

    const latLngs = coordinates.map(
        coordinate => [
            coordinate[1],
            coordinate[0]
        ]
    );

    routeLine = L.polyline(
        latLngs,
        {
            weight: 5
        }
    ).addTo(routeMap);

    originMarker = L.marker([
        route.origin.latitude,
        route.origin.longitude
    ])
    .addTo(routeMap)
    .bindPopup(
        `<strong>Departure</strong><br>${route.origin.name}`
    );

    destinationMarker = L.marker([
        route.destination.latitude,
        route.destination.longitude
    ])
    .addTo(routeMap)
    .bindPopup(
        `<strong>Destination</strong><br>${route.destination.name}`
    );

    routeMap.fitBounds(
        routeLine.getBounds(),
        {
            padding: [40, 40]
        }
    );
}

function hideMessages() {

    routeResult.classList.add("hidden");
    routeError.classList.add("hidden");
}


function showError(message) {

    errorMessage.textContent = message;

    routeError.classList.remove("hidden");
}


function formatDuration(hours) {

    const wholeHours = Math.floor(hours);

    const minutes = Math.round(
        (hours - wholeHours) * 60
    );

    if (wholeHours === 0) {

        return `${minutes} min`;
    }

    if (minutes === 0) {

        return `${wholeHours}h`;
    }

    return `${wholeHours}h ${minutes}m`;
}



if (routeForm) {

    routeForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            hideMessages();

            const origin =
                originInput.value.trim();

            const destination =
                destinationInput.value.trim();


            /* Empty fields */

            if (!origin || !destination) {

                showError(
                    "Please enter both cities."
                );

                return;
            }


            /* Same city */

            if (
                origin.toLowerCase() ===
                destination.toLowerCase()
            ) {

                showError(
                    "Origin and destination must be different."
                );

                return;
            }


            /* Loading state */

            calculateButton.disabled = true;

            calculateButton.textContent =
                "Calculating...";


            try {

                const response = await fetch(
                    "/api/travel/route",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            origin: origin,
                            destination: destination
                        })
                    }
                );


                /* HTTP error */

                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }


                const data =
                    await response.json();


                /* Backend error */

                if (!data.success) {

                    showError(
                        data.error ||
                        "Could not calculate the route."
                    );

                    return;
                }


                /* Save voice message */

                currentVoiceMessage =
                    data.voice_message || "";


                /* Route summary */

                routeSummary.textContent =
                    `${origin} → ${destination}`;


                /* Distance */

                distanceElement.textContent =
                    `${Number(
                        data.distance_km
                    ).toLocaleString()} km`;


                /* Duration */

                durationElement.textContent =
                    formatDuration(
                        Number(data.duration_hours)
                    );


                /* Show result */

                routeResult.classList.remove(
                    "hidden"
                );


                /* Enable / disable speak button */

                if (speakRouteButton) {

                    speakRouteButton.disabled =
                        !currentVoiceMessage;
                }

            }

            catch (error) {

                console.error(
                    "Route error:",
                    error
                );

                showError(
                    "Could not connect to the travel service."
                );
            }

            finally {

                calculateButton.disabled = false;

                calculateButton.textContent =
                    "Calculate route";
            }
        }
    );
}


/* 
   SPEAK ROUTE */

if (speakRouteButton) {

    speakRouteButton.addEventListener(
        "click",
        async function () {

            /* Nothing to speak */

            if (!currentVoiceMessage) {

                return;
            }


            /* Loading state */

            speakRouteButton.disabled = true;

            speakRouteButton.innerHTML =
                "<span>🔊</span> Speaking...";


            try {

                const response = await fetch(
                    "/api/travel/speak",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: currentVoiceMessage
                        })
                    }
                );


                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );
                }


                const data =
                    await response.json();


                if (!data.success) {

                    console.error(
                        "Speak error:",
                        data.error
                    );

                    return;
                }

            }

            catch (error) {

                console.error(
                    "Could not speak route:",
                    error
                );
            }

            finally {

                speakRouteButton.disabled =
                    false;

                speakRouteButton.innerHTML =
                    "<span>🔊</span> Speak route";
            }
        }
    );
}

/* =========================================================
   INITIAL STATE
   ========================================================= */

hideMessages();

if (speakRouteButton) {

    speakRouteButton.disabled = true;
}