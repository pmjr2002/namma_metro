from flask import Flask, render_template, request
import sqlite3

from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/get_hotspot_details', methods=['POST'])
def get_hotspot_details():
    hotspot_name = request.form['hotspot_name']
    conn = sqlite3.connect('metro.db')
    cursor = conn.cursor()
    
    # Execute SQL queries
    cursor.execute("SELECT HID FROM Hotspots WHERE hname=?", (hotspot_name,))
    hid, = cursor.fetchone()
    

    cursor.execute("SELECT EID FROM Exit_Hotspot WHERE HID=?", (hid,))
    eid, = cursor.fetchone()

    cursor.execute("SELECT SID FROM Station_Exit WHERE EID=?", (eid,))
    sid, = cursor.fetchone()

    cursor.execute("SELECT sname FROM Stations WHERE SID=?", (sid,))
    sname, = cursor.fetchone()

    cursor.execute("SELECT ename FROM Exits WHERE EID=?", (eid,))
    ename, = cursor.fetchone()

    cursor.execute("SELECT hname FROM Hotspots WHERE HID=?", (hid,))
    hname, = cursor.fetchone()

    cursor.execute("SELECT line FROM Station_Line WHERE SID=?", (sid,))
    line=''
    temp = cursor.fetchall()
    for i in temp:
        k=i
        x,=k
        line=line+x+','
    line=line[:-1]


    conn.close()

    # Render a separate HTML page with the fetched details
    return render_template('details.html', sname=sname, ename=ename, hname=hname, line=line)

if __name__ == '__main__':
    app.run(debug=True)
