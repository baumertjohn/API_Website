# 100 Days of Code - Day 95 Capstone
# A custom API Based Website
# A website based on data from https://www.openbrewerydb.org/?ref=public-apis

import os

import requests
from flask import Flask, redirect, render_template, request, url_for

# Constants
BREWERY_SEARCH = "https://api.openbrewerydb.org/breweries"
API = os.environ.get("API")

# Globals
brewery_data = []


def get_results(page, search, parameter, sort):
    global brewery_data
    brewery_data = []
    search = search.replace(" ", "_").lower()
    response = requests.get(
        BREWERY_SEARCH, params={"page": page + 1, f"{parameter}": search}
    )
    response.raise_for_status()
    brewery_data_temp = response.json()
    if brewery_data_temp == []:
        next_page = False
        page_number = page + 1
    else:
        next_page = True
        page_number = page + 1
    response = requests.get(
        BREWERY_SEARCH, params={"page": page, f"{parameter}": search, "sort": sort}
    )
    response.raise_for_status()
    brewery_data = response.json()
    return brewery_data, page_number, next_page


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("name_search"):
            search_data = request.form.get("name_search")
            search_parameter = "by_name"
            sort = "name"
        elif request.form.get("city_search"):
            search_data = request.form.get("city_search")
            search_parameter = "by_city"
            sort = "state"
        elif request.form.get("state_search"):
            search_data = request.form.get("state_search")
            search_parameter = "by_state"
            sort = "city"
        if search_data != "Select a State":
            return redirect(
                url_for(
                    "search_results",
                    page_number=1,
                    search_data=search_data,
                    search_parameter=search_parameter,
                    sort=sort,
                )
            )
    return render_template("index.html")


@app.route(
    "/searchresults/<int:page_number>/<search_data>/<search_parameter>/<sort>",
    methods=["GET", "POST"],
)
def search_results(page_number, search_data, search_parameter, sort):
    brewery_data, page_number, next_page = get_results(
        page_number,
        search_data,
        search_parameter,
        sort,
    )
    return render_template(
        "searchresults.html",
        brewery_data=brewery_data,
        page_number=page_number,
        search_data=search_data,
        search_parameter=search_parameter,
        next_page=next_page,
        sort=sort,
    )


@app.route("/brewerydetails/<int:brewery_id>")
def brewery_details(brewery_id):
    print(brewery_data[brewery_id - 1])
    return render_template(
        "brewerydetails.html", brewery=brewery_data[brewery_id - 1], api=API
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
