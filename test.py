from flask import Flask, jsonify
from flask_simple_geoip import SimpleGeoIP
from flask_geoip import GeoIP

app = Flask(__name__)
app.config["GEOIP_CACHE"] = "MEMORY_CACHE"
geoip = GeoIP(app)


@app.route('/')
def test():
    # Retrieve geoip data for the given requester

    return jsonify(geoip.country_name_by_addr('1.2.3.4'))


app.run()