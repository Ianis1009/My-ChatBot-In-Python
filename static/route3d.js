let route3DScene = null;
let route3DCamera = null;
let route3DRenderer = null;

let route3DAnimation = null;

let route3DStartPoint = null;
let route3DEndPoint = null;
let route3DLine = null;

let route3DDragging = false;

let route3DPreviousMouseX = 0;
let route3DPreviousMouseY = 0;

let route3DRotationX = 0.45;
let route3DRotationY = 0.25;

let route3DZoom = 1;


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeRoute3D() {

    const container =
        document.getElementById(
            "route-3d-container"
        );

    if (!container) {
        return;
    }

    if (route3DScene) {
        return;
    }


    /* SCENE */

    route3DScene =
        new THREE.Scene();


    /* CAMERA */

    route3DCamera =
        new THREE.PerspectiveCamera(
            50,
            container.clientWidth /
            container.clientHeight,
            0.1,
            5000
        );


    route3DCamera.position.set(
        0,
        120,
        220
    );


    /* RENDERER */

    route3DRenderer =
        new THREE.WebGLRenderer({
            antialias: true,
            alpha: true
        });


    route3DRenderer.setPixelRatio(
        Math.min(
            window.devicePixelRatio,
            2
        )
    );


    route3DRenderer.setSize(
        container.clientWidth,
        container.clientHeight
    );


    container.appendChild(
        route3DRenderer.domElement
    );


    /* LIGHT */

    const ambientLight =
        new THREE.AmbientLight(
            0xffffff,
            1.5
        );

    route3DScene.add(
        ambientLight
    );


    /* GRID */

    const grid =
        new THREE.GridHelper(
            500,
            40,
            0x334155,
            0x1e293b
        );

    grid.position.y = -8;

    route3DScene.add(
        grid
    );


    /* MOUSE */

    container.addEventListener(
        "mousedown",
        onRoute3DMouseDown
    );

    container.addEventListener(
        "mousemove",
        onRoute3DMouseMove
    );

    container.addEventListener(
        "mouseup",
        onRoute3DMouseUp
    );

    container.addEventListener(
        "mouseleave",
        onRoute3DMouseUp
    );


    container.addEventListener(
        "wheel",
        onRoute3DWheel,
        {
            passive: false
        }
    );


    /* RESIZE */

    window.addEventListener(
        "resize",
        resizeRoute3D
    );


    /* START ANIMATION */

    animateRoute3D();
}


/* =========================================================
   DISPLAY ROUTE
   ========================================================= */

function displayRoute3D(route) {

    if (
        !route ||
        !route.geometry ||
        !route.geometry.coordinates
    ) {
        return;
    }


    initializeRoute3D();


    if (!route3DScene) {
        return;
    }


    /*
       Remove previous route
    */

    if (route3DLine) {

        route3DScene.remove(
            route3DLine
        );

        route3DLine.geometry.dispose();

        route3DLine.material.dispose();

        route3DLine = null;
    }


    if (route3DStartPoint) {

        route3DScene.remove(
            route3DStartPoint
        );

        route3DStartPoint.geometry.dispose();

        route3DStartPoint.material.dispose();

        route3DStartPoint = null;
    }


    if (route3DEndPoint) {

        route3DScene.remove(
            route3DEndPoint
        );

        route3DEndPoint.geometry.dispose();

        route3DEndPoint.material.dispose();

        route3DEndPoint = null;
    }


    const coordinates =
        route.geometry.coordinates;


    if (coordinates.length < 2) {
        return;
    }


    /*
       Convert geographic coordinates
       into a local 3D coordinate system.

       We don't need real-world scale here.
    */

    const first =
        coordinates[0];


    const last =
        coordinates[
            coordinates.length - 1
        ];


    const centerLongitude =
        (first[0] + last[0]) / 2;


    const centerLatitude =
        (first[1] + last[1]) / 2;


    const scale =
        10000;


    const points =
        coordinates.map(
            function (coordinate) {

                const longitude =
                    coordinate[0];

                const latitude =
                    coordinate[1];


                const x =
                    (
                        longitude -
                        centerLongitude
                    ) * scale;


                const z =
                    -(
                        latitude -
                        centerLatitude
                    ) * scale;


                /*
                   Small vertical variation
                   makes the route feel 3D.
                */

                const y =
                    Math.sin(
                        pointsIndex(
                            coordinate,
                            coordinates
                        ) * 0.12
                    ) * 2;


                return new THREE.Vector3(
                    x,
                    y,
                    z
                );
            }
        );


    /*
       ROUTE LINE
    */

    const geometry =
        new THREE.BufferGeometry()
            .setFromPoints(points);


    const material =
        new THREE.LineBasicMaterial({
            color: 0x60a5fa
        });


    route3DLine =
        new THREE.Line(
            geometry,
            material
        );


    route3DScene.add(
        route3DLine
    );


    /*
       START POINT
    */

    route3DStartPoint =
        createRoute3DPoint(
            points[0],
            0x4ade80
        );


    route3DScene.add(
        route3DStartPoint
    );


    /*
       END POINT
    */

    route3DEndPoint =
        createRoute3DPoint(
            points[points.length - 1],
            0x60a5fa
        );


    route3DScene.add(
        route3DEndPoint
    );


    /*
       Center camera on route
    */

    route3DCamera.position.set(
        0,
        100,
        220
    );


    route3DRotationX =
        0.45;

    route3DRotationY =
        0.25;

    route3DZoom =
        1;


    /*
       Show section
    */

    const section =
        document.getElementById(
            "route-3d-section"
        );


    if (section) {

        section.classList.remove(
            "hidden"
        );
    }


    /*
       Fix canvas dimensions
    */

    resizeRoute3D();
}


/* =========================================================
   CREATE POINT
   ========================================================= */

function createRoute3DPoint(
    position,
    color
) {

    const geometry =
        new THREE.SphereGeometry(
            4,
            24,
            24
        );


    const material =
        new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.4
        });


    const sphere =
        new THREE.Mesh(
            geometry,
            material
        );


    sphere.position.copy(
        position
    );


    return sphere;
}


/* =========================================================
   FIND INDEX
   ========================================================= */

function pointsIndex(
    coordinate,
    coordinates
) {

    return coordinates.indexOf(
        coordinate
    );
}


/* =========================================================
   ANIMATION
   ========================================================= */

function animateRoute3D() {

    route3DAnimation =
        requestAnimationFrame(
            animateRoute3D
        );


    if (!route3DScene ||
        !route3DCamera ||
        !route3DRenderer) {

        return;
    }


    /*
       Slowly rotate route
       when user is not dragging.
    */

    if (!route3DDragging) {

        route3DRotationY +=
            0.0008;
    }


    const distance =
        220 /
        route3DZoom;


    route3DCamera.position.x =
        Math.sin(
            route3DRotationY
        ) * distance;


    route3DCamera.position.z =
        Math.cos(
            route3DRotationY
        ) * distance;


    route3DCamera.position.y =
        90 +
        Math.sin(
            route3DRotationX
        ) * 80;


    route3DCamera.lookAt(
        0,
        0,
        0
    );


    /*
       Animate endpoint slightly
    */

    if (route3DEndPoint) {

        route3DEndPoint.scale.setScalar(
            1 +
            Math.sin(
                Date.now() * 0.004
            ) * 0.12
        );
    }


    route3DRenderer.render(
        route3DScene,
        route3DCamera
    );
}


/* =========================================================
   MOUSE CONTROLS
   ========================================================= */

function onRoute3DMouseDown(
    event
) {

    route3DDragging = true;

    route3DPreviousMouseX =
        event.clientX;

    route3DPreviousMouseY =
        event.clientY;
}


function onRoute3DMouseMove(
    event
) {

    if (!route3DDragging) {
        return;
    }


    const deltaX =
        event.clientX -
        route3DPreviousMouseX;


    const deltaY =
        event.clientY -
        route3DPreviousMouseY;


    route3DRotationY +=
        deltaX * 0.008;


    route3DRotationX +=
        deltaY * 0.008;


    route3DRotationX =
        Math.max(
            -1.2,
            Math.min(
                1.2,
                route3DRotationX
            )
        );


    route3DPreviousMouseX =
        event.clientX;

    route3DPreviousMouseY =
        event.clientY;
}


function onRoute3DMouseUp() {

    route3DDragging =
        false;
}


/* =========================================================
   ZOOM
   ========================================================= */

function onRoute3DWheel(
    event
) {

    event.preventDefault();


    if (event.deltaY < 0) {

        route3DZoom *=
            1.08;

    } else {

        route3DZoom *=
            0.92;
    }


    route3DZoom =
        Math.max(
            0.5,
            Math.min(
                3,
                route3DZoom
            )
        );
}


/* =========================================================
   RESIZE
   ========================================================= */

function resizeRoute3D() {

    const container =
        document.getElementById(
            "route-3d-container"
        );


    if (
        !container ||
        !route3DCamera ||
        !route3DRenderer
    ) {

        return;
    }


    const width =
        container.clientWidth;


    const height =
        container.clientHeight;


    if (!width || !height) {
        return;
    }


    route3DCamera.aspect =
        width / height;


    route3DCamera.updateProjectionMatrix();


    route3DRenderer.setSize(
        width,
        height
    );
}