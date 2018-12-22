from bottle import template
import requests
import json

JSON_FOLDER = './data'
AVAILABE_SHOWS = ["7", "66", "73", "82", "112", "143", "175", "216", "1371", "1871", "2993", "305"]
URL_API = "http://api.tvmaze.com/shows/"


def getVersion():
    return "0.0.1"


def getJsonFromFile(showName):
    try:
        return json.loads(template("{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName)))

    # Sacha's improvement, if it bugs change here
    except Exception as e:
        print(e)
        return "{}"


def getListOfShows():
    result = [getJsonFromFile(x) for x in AVAILABE_SHOWS]
    return result
