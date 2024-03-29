from flask import Flask, render_template, request
import sqlite3

from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/')
def land():
    return render_template('landing.html')

@app.route('/templates/contactus.html')
def contactus():
    return render_template('contactus.html')

@app.route('/templates/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

@app.route('/templates/trip.html')
def trip():
    return render_template('trip.html')

@app.route('/index')
def ind():
    return render_template('index.html')

@app.route('/get_hotspot_details', methods=['POST'])
def get_hotspot_details():
    hotspot_name = request.form['hotspot_name']
    
    # Validate input
    if not hotspot_name:
        return "Hotspot name cannot be empty"
    # Optionally, you can add more validation logic here, such as checking for length, allowed characters, etc.
    
    conn = sqlite3.connect('metro.db')
    cursor = conn.cursor()
    
    try:
        # Execute SQL queries
        cursor.execute("SELECT HID FROM Hotspots WHERE hname=?", (hotspot_name,))
        result = cursor.fetchone()

        if result is None:
            return "Hotspot not found"

        hid, = result

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
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
