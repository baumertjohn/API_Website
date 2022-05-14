# 100 Days of Code - Day 95 Capstone
# A custom API Based Website
# A website based on data from https://www.openbrewerydb.org/?ref=public-apis

from flask import Flask, redirect, render_template, request, url_for
import requests
import os

# Constants
BREWERY_SEARCH = "https://api.openbrewerydb.org/breweries"
API = os.environ.get("API")

# Globals
brewery_data = []


def get_results(search, parameter):
    global brewery_data
    search = search.replace(" ", "_").lower()
    response = requests.get(BREWERY_SEARCH, params={"page": 0, f"{parameter}": search})
    response.raise_for_status()
    brewery_data = response.json()
    print(brewery_data[0])
    return brewery_data


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("name_search"):
            name_search = request.form.get("name_search")
            brewery_data = get_results(name_search, "by_name")
        elif request.form.get("city_search"):
            city_search = request.form.get("city_search")
            brewery_data = get_results(city_search, "by_city")
        elif (request.form.get("state_search") != "Select a State") and (
            request.form.get("state_search") != None
        ):
            state_search = request.form.get("state_search")
            brewery_data = get_results(state_search, "by_state")
        return render_template("searchresults.html", brewery_data=brewery_data)
    return render_template("index.html")


@app.route("/searchresults")
def search_results():
    return render_template("searchresults.html")


@app.route("/brewerydetails/<int:brewery_id>")
def brewery_details(brewery_id):
    print(brewery_data[brewery_id - 1])
    return render_template(
        "brewerydetails.html", brewery=brewery_data[brewery_id - 1], api=API
    )


if __name__ == "__main__":
    app.run(debug=True)
