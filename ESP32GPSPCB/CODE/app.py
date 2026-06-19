from flask import Flask, render_template

app = Flask(__name__)

# GPS COORDINATES -> X/Y TILES
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

@app.route('/')
def home():
    return render_template('index.html')

# Data LISTENER
@app.route('/calculate_tiles', methods=['POST'])
def calculate_tiles():
    data = request.get_json()
    north = data['north']
    south = data['south']
    east = data['east']
    west = data['west']
    zoom = data['zoom']

    min_x, min_y = deg2num(south, east, zoom)

    max_x, max_y = deg2num(north, west, zoom)

    
    total_x = (max_x - min_x) + 1
    total_y = (max_y - min_y) + 1
    total_tiles = total_x * total_y

    #logging PYTHON

    print(f"grid X: {min_x}, to {max_x}")
    print(f"grid Y: {min_y}, to {max_y}")
    print(f"Total Tiles to Download: {total_tiles}")

    #response message

    return jsonify({
        "status": "success",
        "total_tiles": total_tiles,
        "message": f"Calculated {total_tiles} tiles for the specified area and zoom level."
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)