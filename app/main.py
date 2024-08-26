from flask import Flask, request, render_template, jsonify
from skyfield.api import load, N, W, wgs84
import geocoder

app = Flask(__name__)
eph = load('de421.bsp')

@app.route('/', methods=['GET', 'POST'])
def index():
    planets = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            position = get_planet_position(body)
            return jsonify(position)
    return render_template('index.html', planets=planets)

def get_planet_position(body):
    ts = load.timescale()
    t = ts.now()
    planets = {
        'mercury': 'mercury', 
        'venus': 'venus', 
        'mars': 'mars', 
        'jupiter': 'jupiter barycenter', 
        'saturn': 'saturn barycenter', 
        'uranus': 'uranus barycenter', 
        'neptune': 'neptune barycenter'}
    planet = eph[planets[body]]
    earth = eph['earth']

    ip_loc = geocoder.ip('me')

    user_pos = earth + wgs84.latlon(ip_loc.latlng[0] * N, ip_loc.latlng[1] * W)
    astrometric = user_pos.at(t).observe(planet)
    alt, az, d = astrometric.apparent().altaz()
    return {'altitude': alt.degrees, 'azimuth': az.degrees}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)