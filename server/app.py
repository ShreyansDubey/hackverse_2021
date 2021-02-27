from flask import Flask
import os
app = Flask(__name__)


@app.route('/tile', methods=["GET"])
def get_tile():
    return "Hello World!"


@app.route('/coordinates', methods=["POST"])
def save_coordinate(name):
    return "Hello {}!".format(name)


PORT = os.environ.get("PORT") if os.environ.get("PORT") != None else 3000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
