from sqlite3.dbapi2 import SQLITE_SELECT
from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
TOTAL_COST = 0

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();
        return render_template("buggy-form.html", buggy=record,)
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        power_type= request.form['power_type']
        if not qty_wheels.isdigit():
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record, msg = "The data you entered is incorrect, please ensure it is an integer.")
        if power_type == "petrol":
            TOTAL_COST = + 4
        elif power_type == "fusion":
            TOTAL_COST = + 400
        elif power_type == "steam":
            TOTAL_COST = + 3
        elif power_type == "bio":
            TOTAL_COST = + 5
        elif power_type == "rocket":
            TOTAL_COST = + 16
        elif power_type == "hamster":
            TOTAL_COST = + 3
        elif power_type == "thermo":
            TOTAL_COST = + 300
        elif power_type == "solar":
            TOTAL_COST = + 40
        elif power_type == "wind":
            TOTAL_COST = + 20
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record Updated"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg,)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
