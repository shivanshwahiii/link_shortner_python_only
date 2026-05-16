import url_shortener
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

@app.route("/shorten", methods=["POST"])
def shorten_url():
    url = request.json.get("url")
    custom = request.json.get("custom")
    result = url_shortener.shorten(url_shortener.load_data(), url, custom)
    return jsonify({"short_url": result}) if result else ("Code taken", 400)

@app.route("/<code>")
def expand_url(code):
    url_map = url_shortener.load_data()
    if code in url_map:
        url_map[code]["clicks"] += 1
        url_shortener.save_data(url_map)
        return redirect(url_map[code]["url"])
    return "Not found", 404
