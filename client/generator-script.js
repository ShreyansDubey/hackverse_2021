const TILE_SIZE = 256;

class CoordMapType {
    constructor(tileSize) {
        this.tileSize = tileSize;
        this.maxZoom = 15;
        this.minZoom = 10;
    }
    getTile(coord, zoom, ownerDocument) {
        // const img = ownerDocument.createElement('img');
        // img.src = `http://localhost:5000/tile?x=${coord.x}&y=${coord.y}&zoom=${zoom}`
        // img.alt = `${coord.x} ${coord.y} ${zoom}`;
        // img.style.width = this.tileSize.width + "px";
        // img.style.height = this.tileSize.height + "px";
        // img.style.opacity = "40%";
        // return img;
        const div = ownerDocument.createElement("div");
        div.innerHTML = String(coord) + " " + zoom;
        div.style.width = this.tileSize.width + "px";
        div.style.height = this.tileSize.height + "px";
        div.style.fontSize = "10";
        div.style.borderStyle = "solid";
        div.style.borderWidth = "1px";
        div.style.borderColor = "#AAAAAA";
        return div;
    }
    releaseTile(tile) {}
}

function getTileCoordinate(latLng, zoom) {
    const scale = 1 << zoom;
    const worldCoordinate = project(latLng);
    const pixelCoordinate = new google.maps.Point(
        Math.floor(worldCoordinate.x * scale),
        Math.floor(worldCoordinate.y * scale)
    );
    const tileCoordinate = new google.maps.Point(
        Math.floor((worldCoordinate.x * scale) / TILE_SIZE),
        Math.floor((worldCoordinate.y * scale) / TILE_SIZE)
    );
    return tileCoordinate;
}

// The mapping between latitude, longitude and pixels is defined by the web
// mercator projection.
function project(latLng) {
    let siny = Math.sin((latLng.lat() * Math.PI) / 180);
    // Truncating to 0.9999 effectively limits latitude to 89.189. This is
    // about a third of a tile past the edge of the world tile.
    siny = Math.min(Math.max(siny, -0.9999), 0.9999);
    return new google.maps.Point(
        TILE_SIZE * (0.5 + latLng.lng() / 360),
        TILE_SIZE * (0.5 - Math.log((1 + siny) / (1 - siny)) / (4 * Math.PI))
    );


}

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: {
            lat: 12.9716,
            lng: 77.5946
        },
    });

    map.overlayMapTypes.insertAt(
        0,
        new CoordMapType(new google.maps.Size(256, 256))
    );

    map.addListener('click', async (mapsMouseEvent) => {
        lat = mapsMouseEvent.latLng.lat();
        lng = mapsMouseEvent.latLng.lng()
        console.log("clicked", lat, lng);
        tileCoordinate = getTileCoordinate(mapsMouseEvent.latLng, 20)
        console.log("tile", tileCoordinate.x, tileCoordinate.y);
        fetch("http://localhost:5000/generator", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                x: tileCoordinate.x,
                y: tileCoordinate.y
            })
        });
    });
}