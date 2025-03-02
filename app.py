from flask import Flask, request, flash, jsonify, render_template, session, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import MySQLdb.cursors
from flask_cors import CORS  # Allow CORS for Chrome extension

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # 16 MB

CORS(app)  # Enable CORS

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Vutlhari@1732')
app.config['MYSQL_DB'] = 'varsity_applicants'
app.secret_key = os.getenv('SECRET_KEY', '610331')

# Initialize MySQL
mysql = MySQL(app)

@app.before_request
def log_request():
    if request.method == "POST":
        print("Incoming Request Data:", request.form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/')
def home():
    return render_template('profile.html')

# Other Pages (Extensions)
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
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
    institutions = data.getlist('institutions')  # Get the list of selected institutions
    
    # Handle file uploads
    id_document = request.files['id_document']
    results_documents = request.files['results_documents']
    proof_of_payment = request.files['proof_of_payment']
    id_document_parent = request.files.get('id_document_parent')
    proof_of_res = request.files.get('proof_of_res')
    
    hashed_password = generate_password_hash(password)
    selected_institutions = ",".join(institutions)
    
    # Save files to the upload folder
    id_document_filename = secure_filename(id_document.filename)
    id_document.save(os.path.join(app.config['UPLOAD_FOLDER'], id_document_filename))

    results_documents_filename = secure_filename(results_documents.filename)
    results_documents.save(os.path.join(app.config['UPLOAD_FOLDER'], results_documents_filename))

    proof_of_payment_filename = secure_filename(proof_of_payment.filename)
    proof_of_payment.save(os.path.join(app.config['UPLOAD_FOLDER'], proof_of_payment_filename))

    id_document_parent_filename = None
    if id_document_parent:
        id_document_parent_filename = secure_filename(id_document_parent.filename)
        id_document_parent.save(os.path.join(app.config['UPLOAD_FOLDER'], id_document_parent_filename))

    proof_of_res_filename = None
    if proof_of_res:
        proof_of_res_filename = secure_filename(proof_of_res.filename)
        proof_of_res.save(os.path.join(app.config['UPLOAD_FOLDER'], proof_of_res_filename))

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (
                username, password, first_name, second_name, surname, email, phone, gender, 
                applicantTitle, idNumber, postalCode, province, homeLanguage, matricYear, 
                upgrading, nsfasBursary, bday, address, school, nesTitle, nextName, nextsName, 
                nextsurName, nextPhone, nextGender, nextEmail, nextBday, nextAddress, 
                nextPostalCode, whatsapp_number, selected_institutions, id_document, 
                results_documents, proof_of_payment, id_document_parent, proof_of_res
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            username, hashed_password, first_name, second_name, surname, email, phone, gender, 
            applicantTitle, idNumber, postalCode, province, homeLanguage, matricYear, 
            upgrading, nsfasBursary, bday, address, school, nesTitle, nextName, nextsName, 
            nextsurName, nextPhone, nextGender, nextEmail, nextBday, nextAddress, 
            nextPostalCode, whatsapp_number, selected_institutions, id_document_filename, 
            results_documents_filename, proof_of_payment_filename, id_document_parent_filename, proof_of_res_filename
        ))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    except Exception as e:
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

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

            if user and check_password_hash(user[1], password):
                session['username'] = username
                session['id'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

        except Exception as e:
            return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        user = cursor.fetchone()
        cursor.close()
        return render_template('dashboard.html', user=user)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)