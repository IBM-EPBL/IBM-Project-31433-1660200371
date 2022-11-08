from flask import Flask, render_template, request, redirect, url_for, session

import ibm_db
import bcrypt
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=dcl74999;PWD=Px6tqEmXL9AcQigs ",'','')

# url_for('static', filename='style.css')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET'])
def home():
    if 'email' not in session:
      return redirect(url_for('login'))
    return render_template('Home.html',name='Home')

@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    if not email or not username  or not password:
      return render_template('Register.html',error='Please fill all fields')
    
    hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    query = "SELECT * FROM USER WHERE email=? "
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO USER(EMAIL, USERNAME,PASSWORD) VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, email)
      ibm_db.bind_param(prep_stmt, 2, username)
      ibm_db.bind_param(prep_stmt, 3, hash)
      ibm_db.execute(prep_stmt)
      return render_template('Register.html',success="You can login")
    else:
      return render_template('Register.html',error='Invalid Credentials')

  return render_template('Register.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('Login.html',error='Please fill all fields')
      query = "SELECT * FROM USER WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('Login.html',error='Invalid Credentials')
      
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('Login.html',error='Invalid Credentials')

      session['email'] = isUser['EMAIL']
      return redirect(url_for('home'))

    return render_template('Login.html',name='Home')

@app.route("/apply",methods=['GET','POST'])
def apply():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form['email']
    mobile = request.form['mobile']
    age = request.form['age']
    gender = request.form['gender']
    blood_group = request.form['blood_group']
    aadhar = request.form['aadhar']
    state = request.form['state']
    city = request.form['city']
    password = request.form['password']

    if not name or not email or not mobile or not age or not gender or not blood_group or not aadhar or not state or not city or not password:
      return render_template('Apply.html',error='Please fill all fields')

    hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    query = "SELECT * FROM appliedusers WHERE email=? OR password=?;"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO appliedusers(NAME, EMAIL, MOBILE, AGE, GENDER, BLOOD_GROUP, AADHAR, STATE, CITY, PASSWORD) VALUES(?,?,?,?,?,?,?,?,?,?);"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, mobile)
      ibm_db.bind_param(prep_stmt, 4, age)
      ibm_db.bind_param(prep_stmt, 5, gender)
      ibm_db.bind_param(prep_stmt, 6, blood_group)
      ibm_db.bind_param(prep_stmt, 7, aadhar)
      ibm_db.bind_param(prep_stmt, 8, state)
      ibm_db.bind_param(prep_stmt, 9, city)
      ibm_db.bind_param(prep_stmt, 10, password)
      ibm_db.execute(prep_stmt)
      return render_template('Apply.html',success="Successfully Registered")
    else:
      return render_template('Apply.html',error='Please check the details you have entered')

  return render_template('Apply.html',name='Home')

@app.route("/rqst",methods=['GET','POST'])
def rqst():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form['email']
    mobile = request.form['mobile']
    age = request.form['age']
    sex = request.form.get('sex')
    blood_group = request.form.get('blood_group')
    address = request.form['address']
    date = request.form.get('date')

    insert_sql = "insert into requsers (name,email,number,age,sex,blood_group,address,date) values (?,?,?,?,?,?,?,?);"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, email)
    ibm_db.bind_param(prep_stmt, 3, mobile)
    ibm_db.bind_param(prep_stmt, 4, age)
    ibm_db.bind_param(prep_stmt, 5, sex)
    ibm_db.bind_param(prep_stmt, 6, blood_group)
    ibm_db.bind_param(prep_stmt, 7, address)
    ibm_db.bind_param(prep_stmt, 8, date)
    ibm_db.execute(prep_stmt)
    return render_template('request.html',success="Successfully Registered")

  return render_template('request.html',name='Home')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)
