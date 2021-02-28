from flask import Flask, request, send_file
from color_map import apply_colormap
from io import BytesIO
from PIL import Image
import os
import numpy as np
import datetime
from flask_pymongo import PyMongo
from json import loads
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
def updateMapVal(x, y, count=1):
    global current_map
    x = x - 366 * 2 ** 11
    y = y - 237 * 2 ** 11
    print("x", x, "y", y)
    if x < 0 or x >= 2**11 or y < 0 or y >= 2**11:
        print("out of bound")
        return
    
    if current_map[x, y] + count < 255:
        current_map[x, y] += count
        print("updated", x, y, current_map[x, y])
    else:
        current_map[x, y] = 255
        print("max reached")

def init_current_map():
    global current_map
    try:
        current_map = np.load('map.npy')
    except:
        # current_map = (np.random.rand(map_size, map_size) * 255).astype(np.uint8)
        current_map = np.zeros((map_size, map_size), dtype=np.uint8)
        # current_map[0:100, 0:100] = 100
        # current_map[100:200, 100:200] = 200

def smooth_tiles(x, y, initial_weight) :
    x_neighbor_coords = [x + d for d in range(-5,6)]
    y_neighbor_coords = [y + d for d in range(-5,6)]

    for x_n in x_neighbor_coords:
        for y_n in y_neighbor_coords: 
            if ( x_n != x and y_n != y) :
                man_distance = abs(x - x_n) + abs(y - y_n)
                weight = initial_weight / (2 ** man_distance)
                print(initial_weight, weight)
                updateMapVal(x_n, y_n, weight)



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
    x = int(request.json['x'])
    y = int(request.json['y'])

    
    updateMapVal(x, y, 2)

    # Adjecent neighbours
    updateMapVal(x, y + 1)
    updateMapVal(x, y - 1)
    updateMapVal(x + 1, y)
    updateMapVal(x - 1, y)

    # Diagonal neighbours
    updateMapVal(x + 1, y + 1)
    updateMapVal(x + 1, y - 1)
    updateMapVal(x - 1, y - 1)
    updateMapVal(x - 1, y + 1)

    return ('', 204)

@app.route('/generator', methods=["POST"])
def generator():
    x = int(request.json['x'])
    y = int(request.json['y'])

    updateMapVal(x, y, 100)

    # # Adjecent neighbours
    # updateMapVal(x, y + 1, 40)
    # updateMapVal(x, y - 1, 40)
    # updateMapVal(x + 1, y, 40)
    # updateMapVal(x - 1, y, 40)

    # # Diagonal neighbours
    # updateMapVal(x + 1, y + 1, 20)
    # updateMapVal(x + 1, y - 1, 20)
    # updateMapVal(x - 1, y - 1, 20)
    # updateMapVal(x - 1, y + 1, 20)
    smooth_tiles(x, y, 100)

    return ('', 204)


@app.route('/pickle', methods=["GET"])
def pickle():
    global current_map
    with open("map.npy", 'w') as f:
        current_map.save(f)
    


PORT = os.environ.get("PORT") if os.environ.get("PORT") != None else 5000
if __name__ == '__main__':
    init_current_map()
    app.run(host='0.0.0.0', port=PORT)
