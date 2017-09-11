from flask import Flask
from flask import render_template
from flask import request
import json

import dbconfig
if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper

@app.route('/test')
def test():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print (e)
        # getting error - get_all_inputs() missing 1 required positional argument: 'self'
        data = None
    return render_template("home.html", data=data)

@app.route("/")
def home():
    # crimes = DB.get_all_crimes()
    # getting error - get_all_crimes() missing 1 required positional argument: 'self'
    # hardcoded crimes
    crimes = [{'latitude':37.3215697595007,
                 'longitude':-121.97733879089355,
                 'date':"2000-01-01",
                 'category':"mugging",
                 'description':'i was mugged'
                 }]
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes)

@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()

@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

if __name__ == '__main__':
    app.run(port=5000, debug=True)