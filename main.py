# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask import jsonify, json
from createDb import Api

api = Api()
app = Flask(__name__,)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin()
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/saved/')
def saved():
    return str(api.getSavedMovies())


@app.route("/here",  methods = ['POST'])
def hello():
    print(request.get_json())
    r = request.get_json()
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

app.run(port=3000,host='0.0.0.0')

