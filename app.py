from flask import Flask, request, jsonify, render_template
from services.scraper import fetch_data
from services.ai import analyze
from database.db import init_db, save, seed_cars, get_all_cars

app = Flask(__name__)

init_db()
seed_cars()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/cars", methods=["GET"])
def get_cars():
    cars = get_all_cars()
    return jsonify(cars)


@app.route("/analyze", methods=["POST"])
def analyze_car():
    data = request.json

    brand = data.get("brand")
    series = data.get("series")
    engine = data.get("engine")  # motor tipi
    package = data.get("package")
    year = data.get("year")

    if not all([brand, series, engine, package, year]):
        return jsonify({"error": "Eksik veri"}), 400

    url = f"https://www.sikayetvar.com/{brand.lower()}"
    comments = fetch_data(url)

    if not comments:
        return jsonify({"error": "Veri bulunamadı"}), 404

    result = analyze(comments, brand, series, engine, package, year)
    save(brand, series, engine, package, year, result)

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
