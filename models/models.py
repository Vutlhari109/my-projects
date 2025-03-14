from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    # Define the fields for the 'users' table
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100))
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    applicantTitle = db.Column(db.String(50))
    idNumber = db.Column(db.String(20), nullable=False)
    postalCode = db.Column(db.String(10))
    province = db.Column(db.String(50))
    homeLanguage = db.Column(db.String(50))
    matricYear = db.Column(db.String(4))
    upgrading = db.Column(db.String(50))
    nsfasBursary = db.Column(db.String(50))
    bday = db.Column(db.Date)
    address = db.Column(db.String(200))
    school = db.Column(db.String(100))
    whatsapp_number = db.Column(db.String(20))
    # You can add other fields as needed (like documents)
    id_document = db.Column(db.String(200))
    results_documents = db.Column(db.String(200))
    proof_of_payment = db.Column(db.String(200))
    id_document_parent = db.Column(db.String(200))
    proof_of_res = db.Column(db.String(200))

    # You can add relationships, methods, or any other logic here

    def __init__(self, username, first_name, second_name, surname, email, phone, gender, applicantTitle, idNumber, postalCode,
                 province, homeLanguage, matricYear, upgrading, nsfasBursary, bday, address, school, whatsapp_number):
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.gender = gender
        self.applicantTitle = applicantTitle
        self.idNumber = idNumber
        self.postalCode = postalCode
        self.province = province
        self.homeLanguage = homeLanguage
        self.matricYear = matricYear
        self.upgrading = upgrading
        self.nsfasBursary = nsfasBursary
        self.bday = bday
        self.address = address
        self.school = school
        self.whatsapp_number = whatsapp_number
