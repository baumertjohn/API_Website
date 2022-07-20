# Brewery Finder Website

## A 100 Days of Code capstone project for Day 95 - A custom API based Website

This project is a website running on a Flask server that displays results from the Open Brewery DB based on whether a user wants to search by "Brewery Name", "City" or "State".  The result are displayed with basic brewery information and a map provided by Google Maps.  Since multiple pages of results can be returned, a solution was needed to set up multiple pages

## How To:

An .env file with following will need to be created:
1. **API** - This is the Google Developer Maps API that needs to created to show map results.

## Demo Website
A working demo can be seen at - https://brewery.baumert.tech/

## Known Issues
Since this is running a basic Flask implementation, more than one user searching will result in incorrect data as the API results are stored in a single list dataset.

