
# hackverse_2021
Project made during Hackverse 2.0 Feb 27th-28th 2021
- Hack Title: **NotAlone**
- Description of the Hack: Sometimes the shortest route is not always the safest. NotAlone helps out by helping people detemine the safety of routes.
    - Overlays Google maps with **colored map tiles**, from isolated to safe (red to green).
    - Anonymous location data collected from people to determine the safety of routes by crowd sourcing
    - Helps people determine the safety of routes at night and while they are travelling to new place
    - System designed using Flask as backend server, the server has endpoints to recieve data from people and for sending overlay images. It generates the overlay images using the most recent data.
    - Map is divided into tiles and each tile has its own score, this score is stored on the server.
    - To render the overlay, server generates the overlay images in tiles based on the map zoom level and location. Overlay images are only loaded after the map tile underneath is loaded, loading only the tiles required

### Implementation Details
- Google maps uses a tiled based approach to optimise map loading from server
	- we utilise this optimization to generate heatmap tiles dynamically and load it onto the user's device
	- Latitude and longitude are converted to **mercator projection** (UTM) coordinated from which tile coordinates are derived.
- On the backend
	- We store anonymous population density data crowdsourced from users per tile
	- If user moves to new tile, new location data is sent to server
	- Tile density data stored in memory
		- fast lookups
		- dynamic live tile generation per user
- Frontend
	- seamless integration with Google Maps
	- tiles are loaded dynamically
		- only for location being viewed
			- reduces data usage


- Dependencies: 
    - `Python==3.7.10`
    - `Flask_Cors==3.0.10`
    - `Flask_PyMongo==2.3.0`
    - `Flask==1.1.2`
    - `numpy==1.19.2`
    - `matplotlib==3.3.2`
    - `Pillow==8.1.0 `


- Installation steps:
    - Install anaconda for your specifc OS [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual)
    - Create a new anaconda environment: `conda create <env_name>`
    - Activate environment: `conda activate <env_name>`
    - Install the required dependencies: `pip install -r requirements.txt`
    - If the above command throws error: `pip install -r requirements.txt --user`
    - Start the server: `cd server && python app.py`
    - Open the `index.html` in browser to demo


- Declaration of previous work: The hack was made completely in the given time
