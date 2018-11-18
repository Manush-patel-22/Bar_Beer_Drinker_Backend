from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
import json

from BarBeerDrinker import database

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/bar', methods = ["GET"])
def get_bars():
    return jsonify(database.get_bars())

@app.route('/api/drinkers', methods = ["GET"])
def get_drinkers():
    return jsonify(database.get_drinkers())

@app.route('/api/bar/<name>', methods = ["GET"])
def find_bar(name):
    try:
        if name is None:
            raise ValueErroe("bar is not specified")
        bar = database.find_bar(name)
        if bar is None:
            return make_response("No bar found with the given name.", 404)
        return jsonify(bar)
    except ValueError as e:
        return make_response(str(e), 400)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/beers_cheaper_than', methods = ["POST"])
def find_beers_cheaper_than():
    body = json.loads(request.data)
    max_price = body['maxPrice']
    return jsonify(database.filter_beers(max_price))

#Bar Page routes 

@app.route('/api/drinkers_largest_spender/<name>', methods = ["GET"])
def top_drinkers_spenders(name):
    try:
        return jsonify(database.largest_spenders(name))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/most_popular/<name>', methods = ["GET"])
def most_poular_beer(name):
    try:
        return jsonify(database.popular_beer(name))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/sell_most_beer/<name>', methods = ["GET"])
def manf_beer(name):
    try:
        return jsonify(database.manf_most_beer(name))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/distribution_by_week/<name>', methods = ["GET"])
def distribution_by_week(name):
    try:
        return jsonify(database.distribution_by_week(name))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/transaction_peak_times_day/<name>', methods = ["GET"])
def transaction_peak_times_day(name):
    try:
        return jsonify(database.time_distribution_for_bar_spending(name))
    except Exception as e:
        return make_response(str(e), 500)


#Drinker 
@app.route('/api/drinker_transaction/<drinker>', methods = ["GET"])
def drinker_transaction(drinker):
    try:
        return jsonify(database.drinker_data(drinker))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/most_ordered_beer/<drinker>', methods = ["GET"])
def most_ordered_beer(drinker):
    try:
        return jsonify(database.top_beers_for_drinker(drinker))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/spending_different_weeks/<drinker>', methods = ["GET"])
def spending_different_weeks(drinker):
    try:
        return jsonify(database.drinker_distribution_week(drinker))
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/api/spending_different_dates/<drinker>', methods = ["GET"])
def spending_different_dates(drinker):
    try:
        return jsonify(database.spending_different_dates(drinker))
    except Exception as e:
        return make_response(str(e), 500)


@app.route('/api/post_bar', methods = ["POST"])
def post_bar():
    requestData = request.get_json()
    name = requestData["name"]
    license = requestData["license"]
    city = requestData["city"]
    phone = requestData["phone"]
    addr = requestData["addr"]
    OpenTime = requestData["OpenTime"]
    CloseTime = requestData["CloseTime"]
    try:
        database.post_bar_db(name, license, city, phone, addr, OpenTime, CloseTime)
        return "OK" #jsonify(database.post_bar_db(requestData))
    except Exception as e:
        print(e)
        return make_response(str(e), 500)

@app.route('/api/delete_bar/<name>', methods = ["DELETE"])
def delete_bar(name):
    try:
        database.delete_bar_db(name)
        return "BAR DELETED"
    except Exception as e:
        print(e)
        return make_response(str(e), 500)
