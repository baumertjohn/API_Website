# 100 Days of Code - Day 95 Capstone
# A custom API Based Website
# A website based on data from https://www.openbrewerydb.org/?ref=public-apis

from flask import Flask, redirect, render_template, request, url_for

# Constants
SEARCH_BY_NAME = "https://api.openbrewerydb.org/breweries?by_name="
SEARCH_BY_CITY = "https://api.openbrewerydb.org/breweries?by_city="
SEARCH_BY_STATE = "https://api.openbrewerydb.org/breweries?by_state="

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("name_search"):
            name_search = request.form.get("name_search")
            print("NAME SEARCH =", name_search)
        elif request.form.get("city_search"):
            city_search = request.form.get("city_search")
            print("CITY SEARCH =", city_search)
        elif (request.form.get("state_search") != "Select a State") and (
            request.form.get("state_search") != None
        ):
            state_search = request.form.get("state_search")
            print("STATE SEARCH =", state_search)
    return render_template("index.html")


@app.route("/searchresults.html")
def search_results():
    pass


@app.route("/brewerydetails.html")
def brewery_details():
    pass


if __name__ == "__main__":
    app.run(debug=True)
