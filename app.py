from sqlite3.dbapi2 import SQLITE_SELECT
from flask import Flask, render_template, request, jsonify
import sqlite3 as sql


# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

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
    TOTAL_COST = 0
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
        tyres = request.form['tyres']
        if not qty_wheels.isdigit():
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record, msg = "The data you entered is incorrect, please ensure it is an integer.")
        if not (int(qty_wheels) % 2) == 0:
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record, msg = "The data you entered is incorrect, please ensure the number of wheels are even.")
        if (int(qty_wheels)) < 4:
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record, msg = "The data you entered is incorrect, please ensure you have more than 4 wheels.")
        if flag_color == flag_color_secondary:
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM buggies")
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record, msg = "The data you entered is incorrect, please ensure the Primary and Secondary flag colours are not the same.")        
        if power_type == "petrol":
            TOTAL_COST = TOTAL_COST + 4
        if power_type == "fusion":
            TOTAL_COST = TOTAL_COST + 400
        if power_type == "steam":
            TOTAL_COST = TOTAL_COST + 3
        if power_type == "bio":
            TOTAL_COST = TOTAL_COST + 5
        if power_type == "electric":
            TOTAL_COST = TOTAL_COST + 20
        if power_type == "rocket":
            TOTAL_COST = TOTAL_COST + 16
        if power_type == "hamster":
            TOTAL_COST = TOTAL_COST + 3
        if power_type == "thermo":
            TOTAL_COST = TOTAL_COST + 300
        if power_type == "solar": 
            TOTAL_COST = TOTAL_COST + 40
        if power_type == "wind":
            TOTAL_COST = TOTAL_COST + 20
        if tyres == "knobbly":
            TOTAL_COST = TOTAL_COST + 15 * int((qty_wheels))
        if tyres == "slick":
            TOTAL_COST = TOTAL_COST + 10 * int((qty_wheels))
        if tyres == "steelband":
            TOTAL_COST = TOTAL_COST + 20 * int((qty_wheels))
        if tyres == "reactive":
            TOTAL_COST = TOTAL_COST + 40 * int((qty_wheels))
        if tyres == "maglev":
            TOTAL_COST = TOTAL_COST + 50 * int((qty_wheels))
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, tyres=?, TOTAL_COST=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, tyres, TOTAL_COST, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = f"Total Cost of the Buggy is {TOTAL_COST}"
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
