import requests
import json
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, send_from_directory

# API key
api_key = "YOUR_API_KEY"

# Flask app
app = Flask(__name__)

# Get weather data
def get_weather_data(city):
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        latitude = location.latitude
        longitude = location.longitude
    except Exception as e:
        print("Error: Could not locate the city.")
        return None

    units = "imperial"
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units={}".format(
        latitude, longitude, api_key, units
    )
    try:
        r = requests.get(url)
        return json.loads(r.text)
    except Exception as e:
        print("Error: Could not retrieve the weather data.")
        return None

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
# home page
def home_page():
    current_location = None
    if request.method == "POST":
        current_location = request.form.get("location")
        weather_data = get_weather_data(current_location)
        return render_template(
            "home.html", current_location=current_location, weather_data=weather_data
        )
    else:
        return render_template("home.html")


@app.route("/about")
# about page
def about_page():
    return render_template("about.html")


@app.route("/assets/img/<path:path>")
# send images url to assets/img
def send_img(path):
    return send_from_directory("assets/img", path)
