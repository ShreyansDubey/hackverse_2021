class CoordMapType {
    constructor(tileSize) {
        this.tileSize = tileSize;
        this.maxZoom = 15;
        this.minZoom = 10;
    }
    getTile(coord, zoom, ownerDocument) {
        const img = ownerDocument.createElement('img');
        img.src = `http://localhost:5000/tile?x=${coord.x}&y=${coord.y}&zoom=${zoom}`
        img.alt = `${coord.x} ${coord.y} ${zoom}`;
        img.style.width = this.tileSize.width + "px";
        img.style.height = this.tileSize.height + "px";
        img.style.opacity = "40%";
        return img;
    }
    releaseTile(tile) {}
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
}