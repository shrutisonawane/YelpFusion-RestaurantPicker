# YelpFusion-RestaurantPicker
**Overview**

This is a simple Python 2.7 program that gives a call to Yelp's Fusion APIs to choose a random restaurant for you, for any given city in the world where Yelp has a presence.

**Dependencies**

1. [urllib](https://docs.python.org/2.7/library/urllib.html#module-urllib) package
* `built-in with Python 2.7`
2. [geopy 1.11.0](https://pypi.python.org/pypi/geopy) package
* `pip install geopy`
3. [requests 2.7.0](https://pypi.python.org/pypi/requests/2.7.0) module
* `pip install requests`

Next, simply run the code as a command line tool:
`python RestoPicker.py`

**Working**

The tool provides a menu driven command line interface that let's the user choose from a default location of "Arizona State University, Tempe" or input a new city. The geopy libray helps find the city's co-ordinates and gives a call to Yelp's Fusion API to return a list of all restaurants for that location. The program then randomly picks a restaurant to visit and also prints it's address.
