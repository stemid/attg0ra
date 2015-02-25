# coding: utf-8
# JSON gränssnitt för Att Göra applikationen.

from __future__ import print_function
from sys import stderr
from json import dumps, loads, JSONEncoder
from datetime import datetime
from ConfigParser import ConfigParser
from bottle import route, run, request, default_app, response, debug
from Todo.Database import Database

# Global åtkomst till databasen
db = Database()

# Global konfiguration
config = ConfigParser()
config.readfp(open('attg0ra.cfg'))
config.read(['attg0ra_local.cfg'])

# Detta används för att serialisera datetime objekt till JSON. Biblioteket
# json klarar normalt sett inte av att hantera datetime objekt så de 
# omvandlas till strängar. 
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)

# Detta är för att angular ska stödja CORS, alltså olika domäner för gränssnitt
# och API. 
@route('/', method='OPTIONS')
@route('/<id:int>', method='OPTIONS')
def options(id=None):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, UPDATE, DELETE, OPTIONS')
    response.add_header('Access-Control-Allow-Headers', 'X-Custom-Header')
    return 

# Lista alla inlägg eller hämta ett enskilt. 
@route('/', method='GET')
@route('/<id:int>', method='GET')
def list(id=None):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'GET')
    response.content_type = 'application/json'

    # Make a list of items to respond with
    response_list = []
    try:
        for (item_id, item_data) in db:
            if id is not None and item_id != id:
                continue
            todo_dict = loads(item_data)
            todo_dict.update({
                'id': item_id
            })
            response_list.append(todo_dict)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    # Return 404 if the list is empty
    if not len(response_list):
        response.status = 404
        return { 'error': 'Not found' }

    # Return JSON data of the list, use the DateEncoder for datetime fields
    return dumps(response_list, cls = DateEncoder)

# Skapa nya inlägg.
@route('/', method='POST')
def create():
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'POST')
    response.content_type = 'application/json'

    created = datetime.now()
    try:
        jsonBody = loads(request.body.getvalue())
        title = jsonBody.get('inputTitle', 'No title')
        todo = jsonBody.get('inputTodo', 'No content')
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    text = dumps({
        'title': title,
        'text': todo,
        'created': created
    }, cls = DateEncoder)

    try:
        db.add_post(title, text)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'OK' }

# Radera ett inlägg.
@route('/<id:int>', method='DELETE')
def delete(id):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'DELETE')
    response.content_type = 'application/json'

    try:
        if db.is_post(id) is False:
            response.status = 404
            return { 'error': 'Not found' }
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    try:
        db.delete_post(id)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'Deleted' }

# Uppdatera ett inlägg
@route('/<id:int>', method='UPDATE')
def update(id):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'UPDATE')
    response.content_type = 'application/json'

    edited = datetime.now()
    try:
        jsonBody = loads(request.body.getvalue())
        title = jsonBody.get('title', 'No title')
        todo = jsonBody.get('text', '')
        created = jsonBody.get('created', datetime.now())
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    try:
        if db.is_post(id) is False:
            response.status = 404
            return { 'error': 'Not found' }
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    data = dumps({
        'id': id,
        'title': title,
        'text': todo,
        'created': created,
        'edited': edited
    }, cls = DateEncoder)

    try:
        db.update_post(id, data)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'Updated' }

if __name__ == '__main__':
    run(
        host = config.get('api', 'host'), 
        port = config.get('api', 'port')
    )
    debug(config.get('api', 'debug'))
else: # Annars antar vi WSGI
    application = default_app()
