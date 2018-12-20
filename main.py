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
    sectionData = [utils.getJsonFromFile(x) for x in utils.AVAILABE_SHOWS]
    sectionData.sort(key=lambda x: x["name"], reverse=False)
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


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})

#run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
run(host='localhost', port=7000)

