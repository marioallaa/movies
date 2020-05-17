"""
COPYRIGHT NOTICE
"""
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask import jsonify, json
from logic import Api
from os import path, walk

extra_dirs = ['static', 'templates', 'data', '.']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
api = Api()
app = Flask(__name__,)
app.config['TEMPLATES_AUTO_RELOAD'] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin()
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/saved/')
def saved():
    return str(api.getSavedMovies())


@cross_origin()
@app.route("/here",  methods = ['POST'])
def hello():
    r = request.get_json()
    if str(r['search']).startswith('adult-'):
        r['isAdult'] = True
        r['search'] = str(r['search'])[6:]
    print(r)
    return jsonify(api.findMovie(
                search=r['search'], 
                popularity=r['popularity'],
                genres=r['genres'],
                adult=r['isAdult'],
                limit=r['limit']))


@cross_origin()
@app.route('/getSuggestion/', methods=['POST', 'GET'])
def suggestMovie():
    if request.method == 'GET':
        return jsonify(api.findMovie())
    else:
        r = request
        print(r.__dict__)
        return jsonify(api.findMovie())
        return jsonify(api.findMovie(
                search=r['search'], 
                popularity=r['popularity'],
                genres=r['genres'],
                adult=r['isAdult'],
                limit=r['limit']))

    

@app.route('/getMore/')
def save():
    return None

l = open('./keys/fullchain.pem', r)
print(l)
ssl = ('./keys/fullchain.pem', './keys/privkey.pem') 
p = 443
app.run(port=p,host='0.0.0.0', ssl_context=ssl, extra_files=extra_files)

