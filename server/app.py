from flask import Flask, request, send_file
from color_map import apply_colormap
from io import BytesIO
from PIL import Image
import os
import numpy as np
import datetime
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://shreyans:hackverse@cluster0.hwwer.mongodb.net/hackverse2021?retryWrites=true&w=majority"
mongo = PyMongo(app)

map_size = 2 ** 11
current_map = None

def getTileFromMap(x_start, x_end, y_start, y_end):
    # zoom should be 20
    x_start = x_start - 366 * (2 ** 11)
    x_end = x_end - 366 * (2 ** 11)
    y_start = y_start - 237 * (2 ** 11)
    y_end = y_end - 237 * (2 ** 11)

    if x_start < 0 or x_end >= 2**11 or y_start < 0 or y_end >= 2**11:
        return None
    return current_map[x_start:x_end, y_start:y_end]

# 127.0.0.1 - - [27/Feb/2021 19:54:23] "GET /tile?x=187528&y=121548&zoom=18 HTTP/1.1" 200 -
def updateMapVal(x, y):
    global current_map
    x = x + 366 * 2 ** 11
    y = y + 237 * 2 ** 11
    
    if current_map[x, y] < 255:
        current_map[x, y] += 1

def init_current_map():
    global current_map
    # current_map = (np.random.rand(map_size, map_size) * 255).astype(np.uint8)
    current_map = np.zeros((map_size, map_size), dtype=np.uint8)
    # current_map[0:100, 0:100] = 100
    # current_map[100:200, 100:200] = 200


@app.route('/tile', methods=["GET"])
def get_tile():
    coordx = int(request.args.get("x"))
    coordy = int(request.args.get("y"))
    zoom = int(request.args.get("zoom"))

    if zoom < 10 or zoom > 20:
        # TODO: generate 256x256 img, alpha 0
        return send_file("empty_tile.png")

    # convert to zoom 20
    zoom_diff = 2 ** (20 - zoom)
    
    x_start = coordx * zoom_diff
    x_end = x_start + zoom_diff
    
    y_start = coordy * zoom_diff
    y_end = y_start + zoom_diff

    tile = getTileFromMap(x_start, x_end, y_start, y_end)

    try:
        tile.shape
    except:
        return send_file("empty_tile.png")
    
    tile = apply_colormap(tile)


    # prepare object for sending
    img = Image.fromarray(tile).transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM).resize((256, 256))

    img.save(f'imgs/{coordx}_{coordy}_{zoom}.png')

    return send_file(f'imgs/{coordx}_{coordy}_{zoom}.png', mimetype='image/png')


@app.route('/coordinates', methods=["POST"])
def save_coordinate():
    latitude = float(request.json['latitude'])
    longitude = float(request.json['longitude'])

    # Scale extrema
    LAT_MAX = 85
    LAT_MIN = -85
    LONG_MAX = 180
    LONG_MIN = -180
    TILE_MAX = 2**20
    TILE_MIN = 0
    
    # Converting lat long to tile coords by linear scaling
    tile_x = (((latitude - LAT_MIN) / (LAT_MAX - LAT_MIN)) * (TILE_MAX - TILE_MIN)) + TILE_MIN
    tile_y = (((longitude - LONG_MIN) / (LONG_MAX - LONG_MIN)) * (TILE_MAX - TILE_MIN)) + TILE_MIN
    
    # Casting to int to round-down
    tile_x = int(tile_x)
    tile_y = int(tile_y)

    # current_date = datetime.datetime.now().strftime("%d_%m_%Y")
    # current_hour = datetime.datetime.now().strftime("%H")

    # Increment specific pixel value in db for current date and time
    updateMapVal(tile_x, tile_y)
    


PORT = os.environ.get("PORT") if os.environ.get("PORT") != None else 5000
if __name__ == '__main__':
    init_current_map()
    app.run(host='0.0.0.0', port=PORT)
