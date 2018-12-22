import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils

# Static Routes


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    sectionData = utils.getListOfShows()
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=sectionData)

@route('/browse/<order>')
def browse(order):
    sectionTemplate = "./templates/browse.tpl"
    sectionData = utils.getListOfShows()
    if order == 'name':
        sectionData.sort(key=lambda x: x["name"], reverse=False)
    elif order == 'ratings':
        sectionData.sort(key=lambda x: x['rating']['average'], reverse=True)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=sectionData)


@route('/show/<showid>')
def browse_show(showid):
    sectionTemplate = "./templates/show.tpl"
    sectionData = utils.getJsonFromFile(int(showid))
    if showid not in utils.AVAILABE_SHOWS:
        return error404(error)
    else:
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=sectionData)


@route('/ajax/show/<showid>')
def browse_show(showid):
    result = utils.getJsonFromFile(int(showid))
    return template("./templates/show.tpl", result=result)


@route('/show/<showid>/episode/<episodeid>')
def browse_show(showid, episodeid):
    sectionTemplate = "./templates/episode.tpl"
    result = utils.getJsonFromFile(int(showid))
    for ep in result['_embedded']['episodes']:
        if ep["id"] == int(episodeid):
            sectionData = ep
        else:
            return error404(error)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=sectionData)


@route('/ajax/show/<showid>/episode/<episodeid>')
def browse_show(showid, episodeid):
    data = utils.getJsonFromFile(int(showid))
    for ep in data['_embedded']['episodes']:
        if ep["id"] == int(episodeid):
            result = ep
    return template("./templates/episode.tpl", result=result)


@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/search', method="POST")
def post_search():
    sectionTemplate = "./templates/search_result.tpl"
    query = request.forms.get('q')
    listOfShows = utils.getListOfShows()
    results = []
    for show in listOfShows:
        for episode in show['_embedded']['episodes']:
            if query in episode["name"] or (episode["summary"] is not None and query in episode["summary"]):
                match = {
                    "showid": show["id"],
                    "episodeid": episode["id"],
                    "text": str(show["name"] + ": " + episode["name"])
                         }
                results.append(match)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={}, query=query, results=results)


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


# run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
run(host='localhost', port=7000)
