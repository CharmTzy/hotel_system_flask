from flask import Flask, render_template, request, redirect, url_for
from dbfunc import getConnection  # Import the getConnection function from dbfunc.py

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    conn = getConnection()
    cursor = conn.cursor()

    email = request.form['email']
    password = request.form['password']

    # Execute a query to check if the user exists in the database
    cursor.execute("SELECT * FROM Users WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        print("User authenticated successfully")
        # User exists, redirect to a success page
        return redirect(url_for('home'))
    else:
        print("Authentication failed")
        # User does not exist, redirect back to login page with an error message
        return redirect(url_for('login', error='Invalid email or password'))

def get_cities():
    cities = []
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT CityName FROM cities") 
        cities_data = cursor.fetchall()
        cities = [city[0] for city in cities_data]
    except mysql.connector.Error as err:
        print("Error fetching cities:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
    return cities

@app.route('/home')
def index():
    print("Rendering hotelbooking.html")
    cities = get_cities()  # Fetch cities from the database
    return render_template('hotelbooking.html', cities=cities)
    
@app.route('/checkin')
def checkin():
    return render_template('checkin.html')
if __name__ == '__main__':
    app.run(debug=True, port=8000)
