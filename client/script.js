class CoordMapType {
    constructor(tileSize) {
        this.tileSize = tileSize;
        this.maxZoom = 15;
        this.minZoom = 10;
    }
    getTile(coord, zoom, ownerDocument) {

        console.log(coord, zoom)
        const div = ownerDocument.createElement("div");
        div.innerHTML = String(coord);
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

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: {
            lat: 41.85,
            lng: -87.65
        },
    });
    
    map.overlayMapTypes.insertAt(
        0,
        new CoordMapType(new google.maps.Size(256, 256))
    );
}