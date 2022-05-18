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
search_data = ""
search_parameter = ""
# page_number = 0


def get_results(page, search, parameter):
    global brewery_data
    brewery_data = []
    search = search.replace(" ", "_").lower()
    response = requests.get(
        BREWERY_SEARCH, params={"page": page + 1, f"{parameter}": search}
    )
    response.raise_for_status()
    brewery_data_temp = response.json()
    if brewery_data_temp == []:
        page_number = -1
    else:
        page_number = page + 1
    response = requests.get(
        BREWERY_SEARCH, params={"page": page, f"{parameter}": search}
    )
    response.raise_for_status()
    brewery_data = response.json()
    return brewery_data, page_number


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("name_search"):
            name_search = request.form.get("name_search")
            # brewery_data, next_page = get_results(name_search, "by_name")
            return redirect(
                url_for(
                    "search_results",
                    page_number=1,
                    search_data=name_search,
                    search_parameter="by_name",
                )
            )
        elif request.form.get("city_search"):
            city_search = request.form.get("city_search")
            brewery_data, next_page = get_results(city_search, "by_city")
        elif request.form.get("state_search") != "Select a State":
            state_search = request.form.get("state_search")
            brewery_data, next_page = get_results(state_search, "by_state")
        try:
            if brewery_data:
                # return redirect(url_for("search_results", page_number=next_page))
                pass
        except UnboundLocalError:
            pass
    return render_template("index.html")


@app.route(
    "/searchresults/<int:page_number>/<search_data>/<search_parameter>",
    methods=["GET", "POST"],
)
def search_results(
    page_number, search_data=search_data, search_parameter=search_parameter
):
    brewery_data, page_number = get_results(page_number, search_data, search_parameter)
    return render_template(
        "searchresults.html",
        brewery_data=brewery_data,
        page_number=page_number,
        search_data=search_data,
        search_parameter=search_parameter,
    )


@app.route("/nextpage")
def next_page_results():
    return


@app.route("/brewerydetails/<int:brewery_id>")
def brewery_details(brewery_id):
    print(brewery_data[brewery_id - 1])
    return render_template(
        "brewerydetails.html", brewery=brewery_data[brewery_id - 1], api=API
    )


if __name__ == "__main__":
    app.run(debug=True)
