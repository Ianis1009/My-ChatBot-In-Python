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

const routeMapContainer =
    document.getElementById("route-map");


let currentVoiceMessage = "";


/* =========================================================
   ROUTE MAP
   ========================================================= */

function initializeRouteMap() {

    if (routeMap) {
        return;
    }

    if (!routeMapContainer) {
        console.error("Route map container was not found.");
        return;
    }

    if (typeof L === "undefined") {
        console.error("Leaflet is not loaded.");
        return;
    }

    routeMap = L.map("route-map");

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(routeMap);
}


/* =========================================================
   DISPLAY ROUTE ON MAP
   ========================================================= */

function displayRouteMap(route) {

    if (!routeMapContainer) {
        return;
    }

    if (!route.geometry ||
        !route.geometry.coordinates ||
        !route.geometry.coordinates.length) {

        console.error(
            "Route geometry is missing."
        );

        return;
    }

    routeMapContainer.classList.remove("hidden");

    initializeRouteMap();

    if (!routeMap) {
        return;
    }


    /* Remove previous route */

    if (routeLine) {

        routeMap.removeLayer(
            routeLine
        );

        routeLine = null;
    }


    /* Remove previous origin marker */

    if (originMarker) {

        routeMap.removeLayer(
            originMarker
        );

        originMarker = null;
    }


    /* Remove previous destination marker */

    if (destinationMarker) {

        routeMap.removeLayer(
            destinationMarker
        );

        destinationMarker = null;
    }


    /*
       OSRM returns:

       [longitude, latitude]

       Leaflet expects:

       [latitude, longitude]
    */

    const coordinates =
        route.geometry.coordinates;


    const latLngs =
        coordinates.map(
            function (coordinate) {

                return [
                    coordinate[1],
                    coordinate[0]
                ];
            }
        );


    /* Draw route */

    routeLine =
        L.polyline(
            latLngs,
            {
                weight: 5
            }
        ).addTo(routeMap);


    /* Origin marker */

    originMarker =
        L.marker([
            route.origin.latitude,
            route.origin.longitude
        ])
        .addTo(routeMap)
        .bindPopup(
            `<strong>Departure</strong><br>${route.origin.name}`
        );


    /* Destination marker */

    destinationMarker =
        L.marker([
            route.destination.latitude,
            route.destination.longitude
        ])
        .addTo(routeMap)
        .bindPopup(
            `<strong>Destination</strong><br>${route.destination.name}`
        );


    /* Fit map to route */

    routeMap.fitBounds(
        routeLine.getBounds(),
        {
            padding: [
                40,
                40
            ]
        }
    );


    /*
       Leaflet sometimes calculates the map size
       incorrectly when the container was hidden.
    */

    setTimeout(
        function () {

            routeMap.invalidateSize();

        },
        100
    );
}


/* =========================================================
   HIDE MESSAGES
   ========================================================= */

function hideMessages() {

    routeResult.classList.add(
        "hidden"
    );

    routeError.classList.add(
        "hidden"
    );
}


/* =========================================================
   ERROR
   ========================================================= */

function showError(message) {

    errorMessage.textContent =
        message;

    routeError.classList.remove(
        "hidden"
    );
}


/* =========================================================
   FORMAT DURATION
   ========================================================= */

function formatDuration(minutes) {

    const totalMinutes =
        Math.round(
            Number(minutes)
        );

    if (
        Number.isNaN(totalMinutes) ||
        totalMinutes < 0
    ) {

        return "—";
    }


    const wholeHours =
        Math.floor(
            totalMinutes / 60
        );


    const remainingMinutes =
        totalMinutes % 60;


    if (wholeHours === 0) {

        return `${remainingMinutes} min`;
    }


    if (remainingMinutes === 0) {

        return `${wholeHours}h`;
    }


    return `${wholeHours}h ${remainingMinutes}m`;
}


/* =========================================================
   ROUTE FORM
   ========================================================= */

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

                const response =
                    await fetch(
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

                /*
                   New backend value:

                   duration_minutes

                   Example:
                   151 → 2h 31m
                */

                durationElement.textContent =
                    formatDuration(
                        data.duration_minutes
                    );


                /* Show result */

                routeResult.classList.remove(
                    "hidden"
                );


                /* Display route on map */

                displayRouteMap(
                    data
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

                calculateButton.disabled =
                    false;

                calculateButton.textContent =
                    "Calculate route";
            }
        }
    );
}


if (speakRouteButton) {

    speakRouteButton.addEventListener(
        "click",
        async function () {

            /* Nothing to speak */

            if (!currentVoiceMessage) {

                return;
            }


            /* Loading state */

            speakRouteButton.disabled =
                true;

            speakRouteButton.innerHTML =
                "<span>🔊</span> Speaking...";


            try {

                const response =
                    await fetch(
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



hideMessages();

if (speakRouteButton) {

    speakRouteButton.disabled =
        true;
}