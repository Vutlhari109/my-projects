from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_cors import CORS  # Allow CORS for Chrome extension

app = Flask(__name__)
CORS(app)  # Enable CORS

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Vutlhari@1732')  # Added fallback
app.config['MYSQL_DB'] = 'varsity_applicants'
app.secret_key = os.getenv('SECRET_KEY', '610331')

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('profile.html')

# Other Pages (Extensions)
@app.route('/index')
def index():
    return render_template('index.html')

# Register Route (Sign-Up)
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    
    # Hash the password for secure storage
    hashed_password = generate_password_hash(password)
    
    # Insert the new user into the database
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))  # Redirect to login after successful registration
    except Exception as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        # Ensure username and password are provided
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT pass_word FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user[0], password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)