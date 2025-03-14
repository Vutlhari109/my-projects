from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
import logging
import traceback
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Allow CORS for Chrome extension
from dotenv import load_dotenv
from flask import current_app as app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import hashlib
from MySQLdb._exceptions import IntegrityError  # Import this at the top
import os
import pymysql
from datetime import datetime



 


# Load environment variables from the .env file
load_dotenv()

# Flask Configuration
app = Flask(__name__)

# Set up custom logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Adding StreamHandler for console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
app.logger.addHandler(console_handler)

CORS(app)  # Enable CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Vutlhari:Vutlhari%401732@localhost/varsity_applicants'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize the database
migrate = Migrate(app, db)



class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(120))
    second_name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    applicantTitle = db.Column(db.String(10))
    idNumber = db.Column(db.String(20))
    postalCode = db.Column(db.String(20))
    province = db.Column(db.String(50))
    homeLanguage = db.Column(db.String(50))
    matricYear = db.Column(db.String(20))
    upgrading = db.Column(db.String(20))
    nsfasBursary = db.Column(db.String(20))
    bday = db.Column(db.Date)
    address = db.Column(db.String(255))
    school = db.Column(db.String(255))
    whatsapp_number = db.Column(db.String(20))
    nextName = db.Column(db.String(120))
    nextsName = db.Column(db.String(120))
    nextsName = db.Column(db.String(120))
    nesTitle = db.Column(db.String(10))
    nextGender = db.Column(db.String(10))
    nextIdNumber = db.Column(db.String(20))
    nextPhone = db.Column(db.String(20))
    nextEmail = db.Column(db.String(120))
    nextAddress = db.Column(db.String(255))
    nextPostalCode = db.Column(db.String(20))
    nextBday = db.Column(db.Date)
    address = db.Column(db.String(255))
    institutions = db.Column(db.String(255))

    
    documents = db.relationship('Document', backref='user', lazy=True)
   
    def __repr__(self):
        return f"<User {self.username}>"
    
class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to User
    id_document = db.Column(db.String(255))
    results_documents = db.Column(db.String(255))
    proof_of_payment = db.Column(db.String(255))
    id_document_parent = db.Column(db.String(255))
    proof_of_res = db.Column(db.String(255))

    def __repr__(self):
        return f"<Document {self.id}>"
    
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.message}>"
    
with app.app_context():
    db.create_all()

# MySQL Configuration (load from .env)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')  # Use 'localhost' as fallback
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')  # Use 'root' as fallback
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'your_default_password_here')  # Replace with fallback
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'varsity_applicants')  # Use 'varsity_applicants' as fallback
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key_here')  # Replace with fallback

# Configure upload folder and allowed extensions
app.config['STATIC_FOLDER'] = 'static'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpg', 'jpeg', 'png', 'gif'}  # Update allowed extensions

# Initialize MySQL
mysql = MySQL(app)

# Function to wrap responses in window.alert()
def alert_response(message, status_code=200):
    return f"<script>window.alert('{message}'); window.history.back();</script>", status_code


# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def safe_str(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')  # Convert datetime to string in 'YYYY-MM-DD' format
    return str(value) if value is not None else None


@app.route('/static/<filename>')
def uploaded_file(filename):
    # Ensure you specify the correct directory where the static files are located
    static_folder = os.path.join(app.root_path, 'static')  # This points to the "static" folder in your project directory
    return send_from_directory(static_folder, filename)


@app.before_request
def log_request():
    if request.method == "POST":
        print("Incoming Request Data:", request.form)

@app.route('/')
def home():
    app.logger.debug('Home page accessed.')  # Logs a debug message when the home page is accessed
    return render_template('index.html')


# Other Pages (Extensions)
@app.route('/form')
def form():
    app.logger.debug('Application form accessed.') 
    return render_template('form.html')

def ensure_upload_folder_exists():
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/file_uploaded')
def file_uploaded():
    return "Files uploaded successfully and paths saved in the database!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()

            if user is None:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

            user_id, hashed_password = user  # Unpacking safely
            if check_password_hash(hashed_password, password):
                session['username'] = username
                session['id'] = user_id
                return redirect(url_for('dashboard'))  
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

    return render_template('login.html')



# Error handling (database simulation)
@app.route('/db_error', methods=['GET'])
def db_error():
    try:
        # Simulating a database error
        raise Exception("Database connection failed!")
    except Exception as e:
        return alert_response(f"Database error: {str(e)}", 500)
    
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)  # Fetch user from database
    
    if not user:
        flash("User not found", "danger")
        return redirect(url_for('staff_dashboard'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.first_name = request.form['first_name']
        user.second_name = request.form.get('second_name', '')  # Optional field
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.gender = request.form.get('gender', '')
        user.applicantTitle = request.form.get('applicantTitle', '')
        user.idNumber = request.form['idNumber']
        user.postalCode = request.form.get('postalCode', '')
        user.province = request.form.get('province', '')
        user.homeLanguage = request.form.get('homeLanguage', '')
        user.matricYear = request.form.get('matricYear', '')
        user.upgrading = request.form.get('upgrading', '')
        user.nsfasBursary = request.form.get('nsfasBursary', '')
        user.bday = request.form.get('bday', '')
        user.address = request.form.get('address', '')
        user.school = request.form.get('school', '')
        user.whatsapp_number = request.form.get('whatsapp_number', '')
        user.nextName = request.form['nextName']
        user.nextsName = request.form.get('nextsName', '')
        user.nextsurName = request.form.get('nextsurName', '')
        user.nesTitle = request.form['nesTitle']
        user.nextGender = request.form.get('nextGender', '')
        user.nextIdNumber = request.form.get('nextIdNumber', '')
        user.nextBday = request.form.get('nextBday', '')
        user.nextPhone = request.form.get('nextPhone', '')
        user.nextEmail = request.form.get('nextEmail', '')
        user.nextAddress = request.form.get('nextAddress', '')
        user.nextPostalCode = request.form.get('nextPostalCode', '')
        user.institutions = request.form.get('institutions', '')
        
        # Handle file uploads
        if 'id_document' in request.files and request.files['id_document'].filename:
            user.id_document = request.files['id_document'].filename

        if 'results_documents' in request.files and request.files['results_documents'].filename:
            user.results_documents = request.files['results_documents'].filename

        if 'proof_of_payment' in request.files and request.files['proof_of_payment'].filename:
            user.proof_of_payment = request.files['proof_of_payment'].filename

        if 'id_document_parent' in request.files and request.files['id_document_parent'].filename:
            user.id_document_parent = request.files['id_document_parent'].filename

        if 'proof_of_res' in request.files and request.files['proof_of_res'].filename:
            user.proof_of_res = request.files['proof_of_res'].filename

        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('staff_dashboard'))
    
    app.logger.debug('Edit user page accessed.') 
    return render_template('edit_user.html', user=user)




@app.route('/delete_message', methods=['POST'])
def delete_message():
    try:
        data = request.get_json()  # Get JSON data from the request
        user_id = data['id']  # Extract the user ID
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Example: Delete the message from the database
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM messages WHERE user_id = %s', (user_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Message deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        files = request.files
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        second_name = data.get('second_name')
        surname = data.get('surname')
        email = data.get('email')
        phone = data.get('phone')
        gender = data.get("gender")
        applicantTitle = data.get('applicantTitle')
        idNumber = data.get('idNumber')
        postalCode = data.get('postalCode')
        province = data.get('province')
        homeLanguage = data.get('homeLanguage')
        matricYear = data.get('matricYear')
        upgrading = data.get('upgrading')
        nsfasBursary = data.get('nsfasBursary')
        bday = data.get('bday')
        address = data.get('address')
        school = data.get('school')
        nesTitle = data.get('nesTitle')
        nextIdNumber = data.get('nextIdNumber')
        nextName = data.get('nextName')
        nextsName = data.get('nextsName')
        nextsurName = data.get('nextsurName')
        nextPhone = data.get('nextPhone')
        nextGender = data.get('nextGender')
        nextEmail = data.get('nextEmail')
        nextBday = data.get('nextBday')
        nextAddress = data.get('nextAddress')
        nextPostalCode = data.get('nextPostalCode')
        whatsapp_number = data.get('whatsapp_number')
        institutions = data.getlist('institutions')

    

        # Ensure the default static folder exists
        os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

        # File uploads
        file_paths = {}
        file_fields = {
            'id_document': files.get('id_document'),
            'results_documents': files.get('results_documents'),
            'proof_of_payment': files.get('proof_of_payment'),
            'id_document_parent': files.get('id_document_parent'),
            'proof_of_res': files.get('proof_of_res'),
        }

        for field, file in file_fields.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['STATIC_FOLDER'], filename).replace("\\", "/")
                file.save(file_path)
                file_paths[field] = file_path

        hashed_password = generate_password_hash(password)
        selected_institutions = ",".join(institutions)

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO users (
                    username, password, first_name, second_name, surname, email, phone, gender, 
                    applicantTitle, idNumber, postalCode, province, homeLanguage, matricYear, 
                    upgrading, nsfasBursary, bday, address, school, nesTitle, nextIdNumber, nextName, nextsName, 
                    nextsurName, nextPhone, nextGender, nextEmail, nextBday, nextAddress, 
                    nextPostalCode, whatsapp_number, selected_institutions
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                username, hashed_password, first_name, second_name, surname, email, phone, gender, 
                applicantTitle, idNumber, postalCode, province, homeLanguage, matricYear, 
                upgrading, nsfasBursary, bday, address, school, nesTitle, nextIdNumber, nextName, nextsName, 
                nextsurName, nextPhone, nextGender, nextEmail, nextBday, nextAddress, 
                nextPostalCode, whatsapp_number, selected_institutions
            ))
            user_id = cur.lastrowid

            cur.execute("""
                INSERT INTO documents (
                    user_id, id_document, results_documents, proof_of_payment, id_document_parent, proof_of_res
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id, file_paths.get('id_document'), file_paths.get('results_documents'), 
                file_paths.get('proof_of_payment'), file_paths.get('id_document_parent'), 
                file_paths.get('proof_of_res')
            ))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
        
        except Exception as e:
            logging.error("Error occurred", exc_info=True)
        return "Internal Server Error", 500

    app.logger.debug('Application form in progress.....') 
    return render_template('login.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_id = request.form['userId']
        message = request.form['message']
        file = request.files.get('file')

        # Ensure the default static folder exists
        os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['STATIC_FOLDER'], filename).replace("\\", "/")
            file.save(file_path)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO messages (user_id, message, file_path, timestamp)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """, (user_id, message, file_path))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/edit_form')
def edit_form():
    if 'username' in session:
        user_id = session['id']
        user = User.query.get(user_id)
        if user:
            return render_template('edit_form.html', user=user)
    return redirect('/login')

@app.route('/chat_history/<int:user_id>')
def chat_history(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT message, file_path, timestamp FROM messages WHERE user_id = %s ORDER BY timestamp ASC", (user_id,))
        messages = cur.fetchall()
        cur.close()

        return jsonify(messages)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        user_id = session.get('id')
        if not user_id:
            return jsonify({'error': 'User not logged in'}), 401

        data = request.form
        files = request.files

        # Update user information
        cur = mysql.connection.cursor()
        cur.execute('''
            UPDATE users SET
                first_name = %s,
                second_name = %s,
                surname = %s,
                email = %s,
                phone = %s,
                gender = %s,
                applicantTitle = %s,
                idNumber = %s,
                postalCode = %s,
                province = %s,
                homeLanguage = %s,
                matricYear = %s,
                upgrading = %s,
                nsfasBursary = %s,
                bday = %s,
                address = %s,
                school = %s,
                nextName = %s,
                nextsName = %s,
                nextsurName = %s,
                nextTitle = %s,
                nextIdNumber = %s,
                nextPhone = %s,
                nextGender = %s,
                nextEmail = %s,
                nextBday = %s,
                nextAddress = %s,
                nextPostalCode = %s,
                whatsapp_number = %s,
                selected_institutions = %s
            WHERE id = %s
        ''', (
            data.get('first_name'), data.get('second_name'), data.get('surname'), data.get('email'),
            data.get('phone'), data.get('gender'), data.get('applicantTitle'), data.get('idNumber'),
            data.get('postalCode'), data.get('province'), data.get('homeLanguage'), data.get('matricYear'),
            data.get('upgrading'), data.get('nsfasBursary'), data.get('bday'), data.get('address'),
            data.get('school'), data.get('nextName'), data.get('nextsName'), data.get('nextsurName'),
            data.get('nextTitle'), data.get('nextIdNumber'), data.get('nextPhone'), data.get('nextGender'),
            data.get('nextEmail'), data.get('nextBday'), data.get('nextAddress'), data.get('nextPostalCode'),
            data.get('whatsapp_number'), ",".join(data.getlist('selected_institutions')), user_id
        ))

        # Handle file uploads
        file_fields = {
            'id_document': files.get('id_document'),
            'results_documents': files.get('results_documents'),
            'proof_of_payment': files.get('proof_of_payment'),
            'id_document_parent': files.get('id_document_parent'),
            'proof_of_res': files.get('proof_of_res'),
        }

        for field, file in file_fields.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['STATIC_FOLDER'], filename).replace("\\", "/")
                file.save(file_path)
                cur.execute(f'UPDATE documents SET {field} = %s WHERE user_id = %s', (file_path, user_id))

        mysql.connection.commit()
        cur.close()

        return jsonify({'success': True, 'message': 'User updated successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/chat.html')
def chat():
    username = request.args.get('username')  # Get username from URL

    if not username:
        return "Error: Username is missing!", 400  # Handle missing username

    return render_template('chat.html', username=username)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        try:
            # Retrieve user information and their associated documents
            cur = mysql.connection.cursor()
            cur.execute('''
                SELECT u.*, d.id_document, d.results_documents, d.proof_of_payment, d.id_document_parent, d.proof_of_res
                FROM users u
                LEFT JOIN documents d ON u.id = d.user_id
                WHERE u.username = %s
            ''', (session['username'],))
            user = cur.fetchone()

            # If the user is not found, return an error
            if user is None:
                return redirect('/login')

            # Format the user data for the template
            user_data = {
                "username": safe_str(user[30]), 
                "first_name": safe_str(user[1]),
                "second_name": safe_str(user[2]),
                "surname": safe_str(user[3]),
                "email": safe_str(user[4]),
                "phone": safe_str(user[5]),
                'gender': safe_str(user[6]),
                'applicantTitle': safe_str(user[7]),
                'idNumber': safe_str(user[8]),
                'postalCode': safe_str(user[9]),
                'province': safe_str(user[10]),
                'homeLanguage': safe_str(user[11]),
                'matricYear': safe_str(user[12]),
                'upgrading': safe_str(user[13]),
                'nsfasBursary': safe_str(user[14]),
                'bday': safe_str(user[15]),  # Convert datetime to string
                'address': safe_str(user[16]),
                'school': safe_str(user[17]),
                'nextTitle': safe_str(user[21]),
                'nextIdNumber': safe_str(user[22]),
                'nextName': safe_str(user[18]),
                'nextsName': safe_str(user[19]),
                'nextsurName': safe_str(user[20]),
                'nextPhone': safe_str(user[23]),
                'nextGender': safe_str(user[24]),
                'nextEmail': safe_str(user[25]),
                'nextBday': safe_str(user[26]),  # Convert datetime to string
                'nextAddress': safe_str(user[27]),
                'nextPostalCode': safe_str(user[28]),
                'whatsapp_number': safe_str(user[29]),
                'selected_institutions': safe_str(user[32]),  # Convert list to string
            }

            # Get the documents for the user
            files = {
                'id_document': safe_str(user[36]),
                'results_documents': safe_str(user[37]),
                'proof_of_payment': safe_str(user[38]),
                'id_document_parent': safe_str(user[39]),
                'proof_of_res': safe_str(user[40])
            }

            # Retrieve the messages sent to this user
            cur.execute("SELECT message, file_path FROM messages WHERE user_id = %s", (user[0],))
            messages = cur.fetchall()

            # Correct the file paths
            corrected_messages = []
            for message, file_path in messages:
                if file_path and file_path.startswith('static/'):
                    file_path = file_path[7:]
                corrected_messages.append((message, file_path))

            # Close the cursor
            cur.close()

            # Pass both the user data, files, and messages to the template
            return render_template('dashboard.html', user=user_data, files=files, messages=corrected_messages)

        except Exception as e:
            print(f"Error: {e}")
            return redirect('/error')  # Redirect to an error page if an issue occurs

    return redirect('/login')  # Redirect to login if the user is not in session

@app.route('/staff_dashboard', methods=['GET'])
def staff_dashboard():
    if 'staff_username' in session:
        cur = mysql.connection.cursor()

        # Fetch users
        cur.execute('SELECT * FROM users ORDER BY id DESC')
        users = cur.fetchall()

        # Fetch documents
        cur.execute('SELECT user_id, id_document, results_documents, proof_of_payment, id_document_parent, proof_of_res FROM documents')
        documents = cur.fetchall()
        cur.close()

        # If no users exist, return an error message
        if not users:
            return "No users found in the database."

        # Convert documents list into a dictionary for easy lookup
        document_dict = {}
        for doc in documents:
            user_id = doc[0]
            # Strip the "static/" part if it exists and store the file name
            document_dict[user_id] = [
                doc[i][7:] if doc[i] and doc[i].startswith('static/') else doc[i] 
                for i in range(1, len(doc))
            ]

        return render_template('staff_dashboard.html', users=users, documents=document_dict)
    
    app.logger.debug('Staff dashboard page accessed.') 
    return redirect('/staff_login')


@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, password FROM staff WHERE username = %s", (username,))
            staff = cur.fetchone()
            cur.close()

            if staff:
                # Hash the entered password using SHA2 (256 bits, same as stored)
                hashed_input_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                # Compare the hashed passwords
                if staff[1] == hashed_input_password:
                    session['staff_username'] = username
                    session['staff_id'] = staff[0]
                    return redirect(url_for('staff_dashboard'))
                else:
                    return jsonify({"success": False, "message": "Invalid credentials"}), 401
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

    app.logger.debug('Staff login page accessed.') 
    return render_template('staff_login.html')





@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    
    app.logger.debug('loggin out.........') 
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)  # Start the Flask app

